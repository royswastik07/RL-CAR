import pygame
import neat
import os
import sys
from car import Car
from track import Track
from configparser import ConfigParser

# Setup basic Pygame for visual steps
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("NEAT Self-Driving Car")
clock = pygame.time.Clock()
track = Track(WIDTH, HEIGHT)

def eval_genomes(genomes, config):
    """
    Runs the simulation for all genomes in the current population.
    No rendering here (headless).
    """
    cars = []
    nets = []
    ge = []

    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        cars.append(Car(track.start_pos, track.start_angle))
        genome.fitness = 0
        ge.append(genome)

    # Simulation loop
    # Fixed number of steps per episode
    max_steps = 1000 
    
    for step in range(max_steps):
        # Handle events and render
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Left click
                    mouse_pos = event.pos
                    for i, (rect, label) in enumerate(track.buttons):
                        if rect.collidepoint(mouse_pos):
                            print(f"Switching to Track {label}...")
                            track.set_track(i)
                            # Signal reset
                            raise StopIteration

        screen.fill((0, 0, 0))
        track.draw(screen)
        
        # 1. Check if all cars are dead
        remain_cars = 0
        for car in cars:
            if car.alive:
                remain_cars += 1
        
        if remain_cars == 0:
            break

        # 2. Update and draw each car
        first_living = True
        for i, car in enumerate(cars):
            if car.alive:
                # Get inputs
                inputs = car.get_data(track.walls) 
                
                # Get output from network
                outputs = nets[i].activate(inputs)
                steering = outputs[0]
                throttle = (outputs[1] + 1) / 2
                
                car.update(steering, throttle, track.walls)
                car.draw(screen)
                
                # Draw sensors ONLY for the first living car to avoid clutter
                if first_living:
                    car.sensors.draw(screen)
                    first_living = False
                
                # Fitness function
                ge[i].fitness += car.speed
                
                # Kill if moving too slowly for a while (stuck/spinning)
                # Give them 50 steps to get up to speed
                if step > 50 and car.speed < 1:
                   car.alive = False
                   ge[i].fitness -= 10 # Stronger penalty for wasting time
                
                if not car.alive:
                    ge[i].fitness -= 50
        
        pygame.display.flip()
        
        # Optional: slow down training to see it?
        clock.tick(60) # Uncomment to cap FPS

def run_visual_simulation(genome, config):
    """
    Replays the best genome visually.
    """
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    car = Car(track.start_pos, track.start_angle)
    
    run = True
    step = 0
    max_steps = 1000
    
    print("Replaying Best Genome...")
    
    while run and step < max_steps:
        clock.tick(60) # 60 FPS for visual
        step += 1
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        if not car.alive:
            break
            
        # Logic
        inputs = car.get_data(track.walls)
        outputs = net.activate(inputs)
        steering = outputs[0]
        throttle = (outputs[1] + 1) / 2
        
        car.update(steering, throttle, track.walls)
        
        # Draw
        track.draw(screen)
        car.draw(screen)
        
        # Draw sensors debug
        # (Optional, maybe draw lines)
        
        pygame.display.flip()

def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)
    
    p = neat.Population(config)
    
    # Reporters
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    
    # Run for 50 generations
    # We iterate manually to render in between
    generations = 50
    # We need a way to reset the population if track changes.
    # Since existing NEAT library doesn't easily support "abort and restart" middle of run,
    # we will just recreate the population loop.
    
    current_gen = 0
    while current_gen < generations:
        print(f"\n--- Generation {current_gen} ---")
        
        # We need to catch the "reset" signal from eval_genomes
        # But neat p.run() manages the loop.
        # So we have to hack it or run 1 gen at a time and check return?
        # Standard neat p.run doesn't return the result of eval_genomes easily unless we raise exception 
        # or use a global flag.
        
        # Let's use a class attribute or global variable for simplicity in this script scope
        # Actually p.run returns None.
        
        # Better approach: 
        # If track changes, we want to START OVER with a NEW population?
        # Or keep same population on new track? 
        # User said "switch tracks", usually implies testing same AI or new training?
        # "Reset the training" was in my plan.
        
        try:
             p.run(eval_genomes, 1)
             current_gen += 1
        except StopIteration:
            # We will raise StopIteration in eval_genomes if reset is needed
            print("Track changed! Resetting population...")
            p = neat.Population(config)
            p.add_reporter(neat.StdOutReporter(True))
            p.add_reporter(stats)
            current_gen = 0
            
        # Visualise best
        if p.best_genome:
             try:
                run_visual_simulation(p.best_genome, config)
             except StopIteration:
                 # Also handle reset during replay
                print("Track changed! Resetting population...")
                p = neat.Population(config)
                p.add_reporter(neat.StdOutReporter(True))
                p.add_reporter(stats)
                current_gen = 0

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-neat.txt')
    run(config_path)
