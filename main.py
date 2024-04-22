import pygame
import product_manager

# Initialize pygame
pygame.init()

# Define constants for GUI
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT = pygame.font.Font(None, 36)


def prompt_for_product(screen):
    inputs = {'name': '', 'price': '', 'quantity': '', 'category': ''}
    labels = ['name', 'price', 'quantity', 'category']
    label_index = 0  
    text = ''  
    input_active = True  
    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if labels[label_index] == 'price':
                        inputs[labels[label_index]] = float(text.strip() or 0.0)
                    else:
                        inputs[labels[label_index]] = text
                    label_index += 1
                    text = ''
                    if label_index >= len(labels):
                        input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
        screen.fill(WHITE)
        if label_index < len(labels):  # Check if label_index is within the range of labels
            draw_text(screen, f"Enter product {labels[label_index]}:", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        else:
            input_active = False  # Stop input if label_index exceeds the range of labels

        draw_text(screen, text, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        pygame.display.flip()
    return inputs['name'], inputs['price'], inputs['quantity'], inputs['category']


# Function to display text on screen
def draw_text(screen, text, pos):
    text_surface = FONT.render(text, True, BLACK)
    rect = text_surface.get_rect(center=pos)
    screen.blit(text_surface, rect)


# Function to prompt user to select a product for deletion or update
def prompt_for_action(screen, action, products):
    selected_id = None
    action_active = True
    while action_active:
        screen.fill(WHITE)
        draw_text(screen, f"Select a product ID to {action}:", (SCREEN_WIDTH // 2, 50))
        for i, prod in enumerate(products):
            draw_text(screen, f"{prod[0]}: {prod[1]}", (SCREEN_WIDTH // 2, 100 + i * 50))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    action_active = False
                elif event.key == pygame.K_BACKSPACE:
                    selected_id = None
                    action_active = False
                elif event.key in [getattr(pygame, f"K_{i}") for i in range(10)]:
                    num = int(event.unicode)
                    if num <= len(products):
                        selected_id = num
                        action_active = False
    return selected_id


def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Product Management System")
    clock = pygame.time.Clock()
    running = True
    menu_active = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        screen.fill(WHITE)
        if menu_active:
            draw_text(screen, "Menu:", (SCREEN_WIDTH // 2, 50))
            draw_text(screen, "1. Insert New Product", (SCREEN_WIDTH // 2, 150))
            draw_text(screen, "2. Retrieve All Products", (SCREEN_WIDTH // 2, 200))
            draw_text(screen, "3. Update a Product", (SCREEN_WIDTH // 2, 250))
            draw_text(screen, "4. Delete a Product", (SCREEN_WIDTH // 2, 300))
            draw_text(screen, "0. Exit", (SCREEN_WIDTH // 2, 350))
            pygame.display.flip()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_1]:
                menu_active = False
                product_data = prompt_for_product(screen)
                product_manager.add_product(*product_data)
                menu_active = True
            elif keys[pygame.K_2]:
                menu_active = False
                products = product_manager.get_products()
                for i, prod in enumerate(products):
                    draw_text(screen, str(prod), (SCREEN_WIDTH // 2, 100 + i * 50))  
                pygame.display.flip()
                pygame.time.delay(2000)
                menu_active = True
            elif keys[pygame.K_3]:
                menu_active = False
                products = product_manager.get_products()
                if len(products) > 0:
                    product_id = prompt_for_action(screen, "update", products)
                    if product_id is not None:
                        updated_details = prompt_for_product(screen)
                        product_manager.update_product(product_id, *updated_details)
                menu_active = True
            elif keys[pygame.K_4]:
                menu_active = False
                products = product_manager.get_products()
                if len(products) > 0:
                    product_id = prompt_for_action(screen, "delete", products)
                    if product_id is not None:
                        product_manager.delete_product(product_id)
                menu_active = True
            elif keys[pygame.K_0]:
                running = False

        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()
