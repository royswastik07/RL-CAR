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
        # Handle events to prevent freeze
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        
        # Draw "Training..." occasionaly
        if step % 50 == 0:
            screen.fill((0, 0, 0))
            font = pygame.font.SysFont('Arial', 30)
            text = font.render(f'Training Generation... Step {step}', True, (255, 255, 255))
            screen.blit(text, (200, 300))
            pygame.display.flip()

        # 1. Check if all cars are dead
        if len(cars) == 0:
            break

        # 2. Update each car
        for i, car in enumerate(cars):
            if car.alive:
                # Get inputs
                inputs = car.get_data(track.walls) 
                # Inputs are [dist_left, dist_center, dist_right] normalized
                
                # Get output from network
                outputs = nets[i].activate(inputs)
                steering = outputs[0] # -1 to 1 (tanh)
                throttle = (outputs[1] + 1) / 2 # Normalize tanh (-1,1) to (0,1) or just use sigmoid in config
                # Config says tanh for default activation, so outputs are -1 to 1.
                # If we want throttle 0-1, we clamp or shift. 
                # Let's map tanh (-1, 1) -> (0, 1) via (x+1)/2
                
                car.update(steering, throttle, track.walls)
                
                # Fitness function
                # Reward for moving forward (distance)
                # Penalty for dying handled in car.update (or here)
                ge[i].fitness += car.speed # Reward speed/distance
                
                # Kill if hitting simple fitness cap or stuck?
                # For now just collision check
                if not car.alive:
                    ge[i].fitness -= 50
                    # We don't remove from list immediately to keep indices aligned? 
                    # actually strictly we iterate and if not alive we skip or remove.
                    # Easier to not remove, just ignore.
                
                # Optional: break early if stuck?

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
    for i in range(generations):
        print(f"\n--- Generation {i} ---")
        # Run 1 generation of training
        p.run(eval_genomes, 1)
        
        # Visualise best
        if p.best_genome:
            run_visual_simulation(p.best_genome, config)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-neat.txt')
    run(config_path)
