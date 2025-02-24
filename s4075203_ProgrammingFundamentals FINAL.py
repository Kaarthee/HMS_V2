#s4075203_kaarthee
import sys
from datetime import datetime, timedelta

# Custom Exceptions
class InvalidGuestNameError(Exception):
    def __init__(self, message="Name should contain only alphabets"):
        super().__init__(message)

class InvalidProductError(Exception):
    def __init__(self, message="Invalid product. Please enter a valid product ID or name"):
        super().__init__(message)

class InvalidQuantityError(Exception):
    def __init__(self, message="Quantity must be a positive integer"):
        super().__init__(message)

class InvalidDateError(Exception):
    def __init__(self, message="Invalid date selection. Please check the dates"):
        super().__init__(message)

# Guest Class
class Guest:
    def __init__(self, ID, name, reward):
        self.ID = ID
        self.name = name
        self.reward = reward
        self.reward_rate = 100
        self.redeem_rate = 1

    def get_id(self):
        return self.ID

    def get_name(self):
        return self.name

    def get_reward(self):
        return self.reward

    def get_reward_rate(self):
        return self.reward_rate

    def get_redeem_rate(self):
        return self.redeem_rate

    def set_reward(self, total_cost):
        return round(total_cost * self.reward_rate / 100)

    def update_reward(self, value):
        self.reward = value

    def display_info(self):
        print(f"ID: {self.ID}, Name: {self.name}, Reward Points: {self.reward}")

# Product Class
class Product:
    def __init__(self, ID, name, price):
        self.ID = ID
        self.name = name
        self.price = price

    def get_ID(self):
        return self.ID

    def get_name(self):
        return self.name

    def get_price(self):
        return self.price

    def display_info(self):
        print(f"ID: {self.ID}, Name: {self.name},  Price: {self.price}")

# ApartmentUnit
class ApartmentUnit(Product):
    def __init__(self, ID, name, price, capacity):
        super().__init__(ID, name, price)
        self.capacity = capacity

    def display_info(self):
        print(f"Apartment ID: {self.ID}, Name: {self.name}, Capacity: {self.capacity}, Price: ${self.price}")

# SupplementaryItem
class SupplementaryItem(Product):
    def display_info(self):
        print(f"Supplementary Item: {self.name}, Price: ${self.price}")

# Bundle Class
class Bundle(Product):
    def __init__(self, ID, name, components, price):
        super().__init__(ID, name, price)
        self.components = components  # list of tuples (component, quantity)

    def display_info(self):
        components_str = ', '.join([f"{component.get_ID()} x{qty}" for component, qty in self.components])
        print(f"Bundle ID: {self.ID}, Name: {self.name}, Components: {components_str}, Price: ${self.price}")


#Record Class
class Records:
    def __init__(self):
        self.guest_list = [] 
        self.product_list = []
        self.order_list = []
        self.supplementary_list = []
        self.apartment_list = []
        self.bundle_list = []

    #Read guest.csv
    def read_guests(self):
        # Load guest data from CSV
        try:
            with open(guest_file, 'r') as file:
                for line in file:
                    guest_data = line.strip().split(',')
                    guest_name = guest_data[1]
                    if guest_name.startswith(' '):
                        guest_name = guest_name.lstrip()
                    guest = Guest(int(guest_data[0]), guest_name, int(guest_data[2]))
                    self.guest_list.append(guest)
            return self.guest_list
        except Exception as e:
            print("Error, file not found", e)

    #Read products.csv
    def read_products(self):
        # Load product data from CSV
        try:
            with open(product_file, 'r') as file:
                for line in file:
                    product_data = line.strip().split(',')
                    product_id = product_data[0]
                    product_name = product_data[1]
                    price = product_data[2]

                    if product_id.startswith('U'):
                        capacity = int(product_data[3])
                        product = ApartmentUnit(product_id, product_name, price, capacity)
                        self.apartment_list.append(product)
                    elif product_id.startswith('SI'):
                        product = SupplementaryItem(product_id, product_name, price)
                        self.supplementary_list.append(product)
                    elif product_id.startswith('B'):
                        components = self.parse_bundle_components(product_data)
                        product = Bundle(product_id, product_name, components, price)
                        self.bundle_list.append(product)
                    self.product_list.append(product)
            return self.product_list
        except Exception as e:
            print("Error, file not found", e)

    #Read orders.csv
    def read_orders(self):
        try:
            with open(order_file, 'r') as file:
                for row in file:
                    line = row.strip().split(', ')
                    if len(line) < 4:
                        print("Invalid order line")
                        row.strip()
                        continue
                    guest_name = line[0].strip()
                    product_data = line[1:-3]
                    total_cost = float(line[-3])
                    earned_rewards = int(line[-2])
                    order_date_time = line[-1]
                    orders = {"guest_name": guest_name,
                            "product_data": product_data,
                            "order_date_time": order_date_time,
                            "total_cost": total_cost,
                            "earned_rewards": earned_rewards
                            } 
                    self.order_list.append(orders)
                    guest_in = self.find_guest(guest_name)
                    if guest_in is not None:
                        self.update_guest_rewards()
            return self.order_list
        except Exception as e:
            print("Error, file not found ", e)

    def update_guest_rewards(self):
        for order in self.order_list:
            guest_name = order['guest_name']
            earned_rewards = order['earned_rewards']
            
            guest = self.find_guest(guest_name)
            if guest:
                guest.update_reward(earned_rewards)
            else:
                print(f"Guest {guest_name} not found.")

    def display_guest_order_history(self, guest_name):
        guest_orders = []
        for i, order in enumerate(self.order_list, 1):
            if order['guest_name'].lower() == guest_name.lower():
                # Collect order details
                order_id = f"Order{i}"
                products_ordered = ", ".join(order['product_data'])
                total_cost = order['total_cost']
                earned_rewards = order['earned_rewards']
                
                # Add to guest's order list
                guest_orders.append([order_id, products_ordered, total_cost, earned_rewards])

        if guest_orders:
            # Display order history in tabular form
            print(f"Order history for {guest_name}:\n")
            print(f"{'Order ID':<10}{'Products Ordered':<50}{'Total Cost':<15}{'Earned Rewards':<15}")
            print("-" * 90)

            for order in guest_orders:
                print(f"{order[0]:<10}{order[1]:<50}{order[2]:<15}{order[3]:<15}")
                print("\n")
        else:
            print(f"No orders found for guest: {guest_name}")

    #Parse bundle
    def parse_bundle_components(self, product_data):
        components = []
        component_data = product_data[3:] 

        for component_str in component_data:
            component_str = component_str.strip()
            if "x" in component_str:
                component_id, quantity = component_str.split('x')
                quantity = int(quantity.strip())
                component_id = component_id.strip()
            else:
                component_id = component_str
                quantity = 1  # Default quantity if not provided

            # Find the corresponding product instance from product_list
            component_instance = next((p for p in self.product_list if p.ID == component_id), None)

            if component_instance:  # Ensure the component exists
                components.append((component_instance, quantity))  # Store product instance and quantity
            else:
                print(f"Warning: Component ID {component_id} not found in product list.")

        return components


    #find guest
    def find_guest(self, search_value):
        for guest in self.guest_list:
            if guest.get_id() == search_value or guest.get_name() == search_value:
                return guest
        return None

    #find product
    def find_product(self, search_value):
        search_value = search_value.strip()  # Ensure the value has no extra spaces
        for product in self.product_list:
            if product.get_ID() == search_value or product.get_name() == search_value:
                return product
        return None

    def list_bundles(self):
        if not self.bundle_list:
            print("No bundles available.")
            return

        for product in self.bundle_list:
            product.display_info()
            
    def list_apartment_units(self):
        for product in self.apartment_list:
            product.display_info()

    def list_supplementary_items(self):
        for product in self.supplementary_list:
            product.display_info()        

    #guest list
    def list_guests(self):
        for guest in self.guest_list:
            guest.display_info()

    #product list
    def list_products(self):
        for product in self.product_list:
            product.display_info()

    #top guest
    def get_top_valuable_guests(self):
        guest_order_totals = {}
        for order in self.order_list:
            guest_name = order['guest_name']
            total_cost = order['total_cost']
            if guest_name in guest_order_totals:
                guest_order_totals[guest_name] += total_cost
            else:
                guest_order_totals[guest_name] = total_cost
        sorted_guests = sorted(guest_order_totals.items(), key=lambda x: x[1], reverse=True)
        return sorted_guests[:3]

    #top valuable product 
    # Get top 3 most popular products
    def get_top_valuable_products(self):
        product_quantities = {}
        for order in self.order_list:
            product_data = order['product_data']
            for product_info in product_data:
                # Split product_info to handle 'quantity x product_id' cases
                if "x" in product_info:
                    # We expect something like "2 x U12swan"
                    quantity_str, product_id = product_info.split('x')
                    quantity = int(quantity_str.strip())  # Convert quantity to an integer
                    product_id = product_id.strip()  # Ensure product_id is properly stripped
                else:
                    # If there's no 'x', assume quantity is 1
                    product_id = product_info.strip()
                    quantity = 1

                # Update the quantity for the product in the product_quantities dictionary
                if product_id in product_quantities:
                    product_quantities[product_id] += quantity
                else:
                    product_quantities[product_id] = quantity

        # Sort products by the quantity sold, descending
        sorted_products = sorted(product_quantities.items(), key=lambda x: x[1], reverse=True)
        return sorted_products[:3]

    #statistics
    def generate_statistics(self):
    # Get top 3 valuable guests and top 3 popular products
        top_guests = self.get_top_valuable_guests()
        top_products = self.get_top_valuable_products()

        # Write the statistics to a text file
        with open('stats.txt', 'w') as file:
            file.write("Top 3 Most Valuable Guests:\n")
            for guest_name, total_amount in top_guests:
                file.write(f"{guest_name}: ${total_amount:.2f}\n")

            file.write("\nTop 3 Most Popular Products:\n")
            for product_id, quantity in top_products:
                product = self.find_product(product_id)
                if product:
                    file.write(f"{product.get_name()}: {quantity} sold\n")
                else:
                    print(f"Warning: Product with ID {product_id} not found")

        print("Statistics generated and saved to stats.txt.")
    
class Order:
    def ___init___(self, g_details, p_details, num_guests, length_of_stay, checkin_date, checkout_date, booking_date, bundles, redeem_amount, red):
        self.g_details = g_details  
        self.p_details = p_details  
        self.num_guests = num_guests
        self.length_of_stay = length_of_stay
        self.checkin_date = checkin_date
        self.checkout_date = checkout_date
        self.booking_date = booking_date
        self.bundles = bundles
        self.supplementary_items = [] 
        self.redeem_amount = redeem_amount  
        self.red = red
    def compute_cost(self):
        original_total_cost = self.p_details.get_price() * self.length_of_stay
        discount = 0
        if self.length_of_stay > 5:
            discount = original_total_cost * 0.10  # 10% discount
        final_total_cost = original_total_cost - discount
        reward = self.g_details.calculate_reward(final_total_cost)
    
        self.g_details.update_reward(reward)
        return original_total_cost, discount, final_total_cost, reward
    
    def display_receipt(self, supplementary_items):
        apartment_sub_total = self.p_details.get_price() * self.length_of_stay
        _, discount, final_total_cost, reward = self.compute_cost()
        #Calculate supplementary items total
        supplementary_total = sum(item.get_price() * quantity for item, quantity in supplementary_items)
        bundle_total = sum(bundle.get_price() for bundle in self.bundles)
        total_cost = final_total_cost + supplementary_total + bundle_total
        reward = round(total_cost)
        #display the receipt
        print("=" * 65)
        print(f"Guests receipt")
        print("=" * 65)
        print(f"Guest name: {self.g_details.get_name()}")
        print(f"Number of guests: {self.num_guests}")
        print(f"Apartment name: {self.p_details.get_name()}")
        print(f"Apartment rate: $ {self.p_details.get_price():.2f} (AUD) per night")
        print(f"Check-in date: {self.checkin_date.strftime('%d-%m-%Y')}")
        print(f"Check-out date: {self.checkout_date.strftime('%d-%m-%Y')}")
        print(f"Length of stay: {self.length_of_stay} nights")
        print(f"Booking date: {self.booking_date.strftime('%d/%m/%Y %H:%M')}")
        print(f"Sub-total (apartment): $ {apartment_sub_total:.2f} (AUD)")
        print("-" * 70)
        if supplementary_items:
            print("Supplementary items")
            print("ID   Name                          Quantity  Unit Price $   Cost $")
            for item, quantity in supplementary_items:
                cost = item.get_price() * quantity  # Multiply by the entered quantity
                print(f"{item.get_product_id()}  {item.get_name():<30}  {quantity}         ${item.get_price():.2f}         ${cost:.2f}")
            print(f"Sub-total (supplementary items): $ {supplementary_total:.2f}")
        else:
            print("No supplementary items ordered.")
        print("-" * 70)
        if self.bundles:
            print("Bundles Ordered")
            print("ID   Name                                   Price $")
            for bundle in self.bundles:
                print(f"{bundle.get_product_id()}  {bundle.get_name():<40}  ${bundle.get_price():.2f}")
            print(f"Sub-total (bundles): $ {bundle_total:.2f}")
        else:
            print("No bundles ordered.")
        print("-" * 70)
        print(f"Discount: $ {discount:.2f} (AUD)")
        print(f"Redeemed Amount: $ {self.redeem_amount:.2f} (AUD)")  # Display redeemed amount
        print(f"Total cost: $ {total_cost:.2f} (AUD)")
        print(f"Earned rewards: {reward}")
        print(f"Reward points to redeem: {self.red}")  # Call get_reward on the found guest
        print("Thank you for your booking!")
        print("We hope you will have an enjoyable stay.")
        print("=" * 65)
        return total_cost, reward


# Operations
class Operations:
    def __init__(self, record):
        self.record = record
        self.guest_list = self.record.read_guests()
        self.product_list = self.record.read_products()
        self.order_list = self.record.read_orders()

    #menu
    def menu(self):
        while True:
            print("Make a booking: 1")
            print("Display existing guests: 2")
            print("Display existing bundles: 3")
            print("Display existing apartments : 4")
            print("Display existing Supplementary Units: 5")
            print("Add or update information of apartment units: 6")
            print("Add or update information of supplementary items: 7")
            print("Add or update information of bundles: 8")
            print("Adjust the reward rate of all guests: 9" )
            print("Adjust the redeem rate of all guests: 10")
            print("Display all orders: 11")
            print("Generate Key statistics: 12")
            print("Display a guest order history: 13")
            print("Exit: 14")
            
            option = input("Enter option: ")
            if option == "1":
                self.make_booking()
            elif option == "2":
                self.record.list_guests()
            elif option == "3":
                self.record.list_bundles()
            elif option == "4":
                self.record.list_apartment_units()
            elif option == "5":
                self.record.list_supplementary_items()
            elif option == "6":
                self.add_update_apartment()
            elif option == "7":
                self.add_update_supplementary_item()
            elif option == "8":
                self.add_update_bundle()
            elif option == "9":
                self.adjust_reward_rate()
            elif option == "10":
                self.adjust_redeem_rate()
            elif option == "11":
                self.display_all_orders()
            elif option == "12":
                self.record.generate_statistics()
            elif option == "13":
                self.display_guest_order_history()
            elif option == "14":
                sys.exit()
            else:
                print("Choose a valid number between 1 and 14") 

    #Display guest order
    def display_guest_order_history(self):
        guest_name = input("Enter the guest name to display order history: ")
        self.record.display_guest_order_history(guest_name)

    #All orders display 
    def display_all_orders(self):
        if len (self.order_list) == 0:
            print("no orders found")
        else:
            for order in self.order_list:
                print(order)

    #saving order
    def save_orders(self, order):
        file = open("orders.csv",'a')
        current_order = ",".join(str(item) for item in order)
        file.write(current_order)
    
    #saving guest
    def save_guest(self):
        try:
            with open("guests.csv", 'w') as file:
                for guest in self.guest_list:
                    file.write(f"{guest.get_id()},{guest.get_name()},{guest.get_reward()}\n")
            print("Guest file updated successfully.")
        except Exception as e:
            print(f"Error updating guest file: {e}")

    #update_bundle
    def add_update_bundle(self):
        bundle_id = input("Enter Bundle ID: ")
        bundle = self.record.find_product(bundle_id)
        components = []
        while True:
            component_id = input("Enter Component ID: ")
            component = self.record.find_product(component_id)
            quantity = int(input(f"Enter quantity of {component.get_name()}: "))
            components.append((component, quantity))

            more_components = input("Do you want to add another component? (yes/no): ").lower()
            if more_components == "no":
                break
        if bundle is None:
            bundle_name = input("Enter Bundle Name: ")
            bundle_price = float(input("Enter Bundle Price: "))
            new_bundle = Bundle(bundle_id, bundle_name, components, bundle_price)
            self.record.product_list.append(new_bundle)
            print("New bundle added successfully.")
        else:
            bundle.components = components
            bundle.price = float(input("Enter new Bundle Price: "))
            print("Bundle updated successfully.")


    #adding apartment
    def add_update_apartment(self):
        apartment_id = input("Enter Apartment ID: ")
        apartment = self.record.find_product(apartment_id)
        if apartment is None:
            apartment_name = input("Enter Apartment Name: ")
            apartment_price = float(input("Enter Apartment Price: "))
            apartment_capacity = int(input("Enter Apartment Capacity: "))
            new_apartment = ApartmentUnit(apartment_id, apartment_name, apartment_price, apartment_capacity)
            self.record.product_list.append(new_apartment)
            print("New apartment added successfully.")
        else:
            apartment.name = input("Enter new Apartment Name: ")
            apartment.price = float(input("Enter new Apartment Price: "))
            apartment.capacity = int(input("Enter new Apartment Capacity: "))
            print("Apartment updated successfully.")


    #booking product 
    def get_booking_product(self):
        while True:
            supplementary_item_id = input("Enter supplementary item ID: ")
            supplementary_item = self.record.find_product(supplementary_item_id)
            if supplementary_item is None or not isinstance(supplementary_item, SupplementaryItem):
                print("Invalid supplementary item ID.")
            else:
                return supplementary_item_id


    #quality quantity 
    def get_booking_quantity(self):
        while True:
            try:
                supplementary_item_quantity = int(input("Enter supplementary quantity: "))
                if supplementary_item_quantity > 0:
                    return supplementary_item_quantity
                else:
                    print("Quantity must be a positive number.")
            except ValueError:
                print("Please enter a valid integer.")


    #getting date
    def get_date(self, prompt):
        while True:
            try:
                date_str = input(prompt)
                return datetime.strptime(date_str, "%d/%m/%Y")
            except ValueError:
                print("Invalid date format. Please use dd/mm/yyyy.")


    #reward rate
    def adjust_reward_rate(self):
        while True:
            try:
                new_reward_rate = float(input("Enter new reward rate (positive number): "))
                if new_reward_rate <= 0:
                    raise ValueError("Reward rate must be positive.")
                for guest in self.record.guest_list:
                    guest.reward_rate = new_reward_rate
                print(f"Reward rate adjusted to {new_reward_rate}% for all guests.")
                break
            except ValueError as e:
                print(f"Invalid input: {e}. Please try again.")

    #redeem rate
    def adjust_redeem_rate(self):
        while True:
            try:
                new_redeem_rate = float(input("Enter new redeem rate (positive number, min 1%): "))
                if new_redeem_rate < 1:
                    raise ValueError("Redeem rate must be at least 1%.")
                for guest in self.record.guest_list:
                    guest.redeem_rate = new_redeem_rate
                print(f"Redeem rate adjusted to {new_redeem_rate}% for all guests.")
                break
            except ValueError as e:
                print(f"Invalid input: {e}. Please try again.")


    #Update supplementary 
    def add_update_supplementary_item(self):
        item_id = input("Enter Supplementary Item ID: ")
        item = self.record.find_product(item_id)
        if item is None:
            # New item
            item_name = input("Enter Supplementary Item Name: ")
            item_price = float(input("Enter Supplementary Item Price: "))
            new_item = SupplementaryItem(item_id, item_name, item_price)
            self.record.product_list.append(new_item)
            print("New supplementary item added successfully.")
        else:
            # Update existing item
            item.name = input("Enter new Item Name: ")
            item.price = float(input("Enter new Item Price: "))
            print("Supplementary item updated successfully.")


    #booking validation
    def make_booking(self):

        # Guest name validation
        while True:
            guest_name = input("Enter guest name: ")
            if not guest_name.isalpha():
                print("Guest name should contain only alphabets.")
            else:
                break
        guest = self.record.find_guest(guest_name)
        if guest is None:
            print("New guest found, adding to guest list.")
            guest_id = len(self.guest_list) + 1
            guest = Guest(guest_id, guest_name, 0)
            self.record.guest_list.append(guest)
        else:
            print(f"Existing guest found, reward points is {guest.get_reward()}" )

        #guest number 
        while True:
            try:
                guest_number = int(input("Enter guest number: "))
                if guest_number > 0:
                    break
                else:
                    print("Guest number should be a positive number.")
            except ValueError:
                print("Please enter a valid number.")

        # Apartment selection
        while True:
            apartmentID = input("Enter apartment ID: ")
            apartment = self.record.find_product(apartmentID)
            if apartment is None or not isinstance(apartment, ApartmentUnit):
                print("Invalid apartment ID.")
            else:
                break
        while True:
                try:
                    apartment_quantity = int(input("Enter quantity: "))
                    break
                except ValueError:
                    print("enter valid number")

        # Dates and length of stay validation
        while True:
            check_in_date = self.get_date("Enter check-in date (dd/mm/yyyy): ")
            check_out_date = self.get_date("Enter check-out date (dd/mm/yyyy): ")
            if check_out_date > check_in_date:
                length_of_stay = (check_out_date - check_in_date).days
                break
            else:
                print("Check-out date must be after check-in date.")

        # Booking date
        booking_date = datetime.now().strftime("%d/%m/%Y %H:%M")

        # Supplementary item selection
        supplementary_item_list = []
        supplementary_item_quantity_list = []

        extra_beds_needed = guest_number - apartment.capacity
        if extra_beds_needed > 0:
            extra_beds_quantity = length_of_stay  # Must match nights
            print(f"Extra beds required: {extra_beds_needed}, for {length_of_stay} nights.")
            supplementary_item = self.record.find_product("SI6")
            supplementary_item_list.append(supplementary_item)
            supplementary_item_quantity_list.append(extra_beds_quantity)
        while True:
            car_park_needed = input("Do you want a car park (yes or no)").lower()
            if car_park_needed == "yes":
                car_park_quantity = length_of_stay  # Minimum nights required for car park
                supplementary_item = self.record.find_product("SI1")
                supplementary_item_list.append(supplementary_item)
                supplementary_item_quantity_list.append(car_park_quantity)
                break
            elif car_park_needed == "no":
                break
            else: print("yes or no")

        # Quantity validation
        while True:
            option = input("Do you want an extra supplementary item?(Yes/No): ").lower()
            if option == "yes":
                supplementary_item_id = self.get_booking_product()
                supplementary_item = self.record.find_product(supplementary_item_id)
                supplementary_item_list.append(supplementary_item)
                supplementary_item_quantity = self.get_booking_quantity()
                supplementary_item_quantity_list.append(supplementary_item_quantity)
            elif option == "no":
                break 
            else: 
                print("Please choose yes or no")
        
        # Calculate costs
        # Subtotal_apartment
        apartment_subtotal = float(apartment.get_price()) * length_of_stay
        # Subtotal apartment
        supplementary_subtotal = 0
        for i in range(len(supplementary_item_list)):
            supplementary_subtotal += float(supplementary_item_list[i].get_price()) * supplementary_item_quantity_list[i]
        
        #Total cost
        total_cost = apartment_subtotal + supplementary_subtotal
        
        #reward point
        reward_points = guest.get_reward()
        if reward_points > 0:
            redeem_money = input("Do you want to redeem the points? ").lower() #redeem amount
            if redeem_money == "yes":
                redeem_amount = (reward_points / guest.get_redeem_rate()) / 100
                final_cost = total_cost - redeem_amount
                final_cost = round(final_cost,2)
                print(f"Applied reward points {reward_points} Redemable amount {redeem_amount}")
            else:
                redeem_amount = reward_points / guest.get_redeem_rate()
                final_cost = total_cost - redeem_amount
                final_cost = round(final_cost,2)#FINAL COST
        reward_earned = guest.set_reward(total_cost)
        guest.update_reward(reward_earned)

        #DISPLAY ORDER
        order = []
        print("=========================================================")
        print(f"Guest name: {guest.get_name()}")
        order.append(guest.get_name())
        print(f"Number of guests: {guest_number}")
        print(f"Apartment Name:{apartment.get_name()}")
        print(f"Aparment quantity: {apartment_quantity}")
        order_apt = f"{apartment_quantity}x{apartment.get_name()}"
        order.append(order_apt)
        print(f"Apartment Rate $: {apartment.get_price()}")
        print(f"Check-in Date: {check_in_date}")
        print(f"Check out date: {check_out_date}")
        print(f"Length of Stay: {length_of_stay}")
        print(f"Booking date: {booking_date}")
        print(f"Apartment Subtotal AUD: {apartment_subtotal}")
        print(f"Supplementary Items:")
        
        si_list = []
        for i in range(len(supplementary_item_list)):
            print(f"Supplementary ID: {supplementary_item_list[i].get_ID()}")
            print(f"Supplementary ID: {supplementary_item_list[i].get_name()}")
            print(f"Supplementary ID: {supplementary_item_quantity_list[i]}")
            print(f"Supplementary ID: {supplementary_item_list[i].get_price()}")
            si_order = f"{supplementary_item_list[i].get_ID()} x {supplementary_item_quantity_list[i]}" 
            si_list.append(si_order)
        supplementary_item_dict = {'product_data': si_list}
        if len(si_list) > 0:
            order.append(supplementary_item_dict)
        print(f"Cost $: {supplementary_subtotal}")
        print(f"Total Cost: {total_cost}")
        if reward_points > 0:
            print(f"Reward points to redeem: {guest.get_reward()}")
            print(f"Discount based on points: {redeem_amount} (AUD)")
            print(f"Final total cost: ${final_cost}")
            order.append(final_cost)
        print(f"Earned rewards: (points){reward_earned}")
        order.append(reward_earned)
        order.append(booking_date)
        self.save_orders(order)
        self.save_guest()
        print(f"Thank you for your booking!")  
        print("We hope you will have an enjoyable stay. ")
        print("=========================================================")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        # No arguments provided, use default file names
        guest_file = 'guests.csv'
        product_file = 'products.csv'
        order_file = 'orders.csv'
    elif len(sys.argv) == 3:
        # Guest and product files provided
        guest_file = sys.argv[1]
        product_file = sys.argv[2]
        order_file = 'orders.csv'  # Default order file if not provided
    elif len(sys.argv) == 4:
        # Guest, product, and order files provided
        guest_file = sys.argv[1]
        product_file = sys.argv[2]
        order_file = sys.argv[3]
    else:
        print("Usage: python script.py [guest_file] [product_file] [order_file(optional)]")
        sys.exit(1)

    record = Records()
    operations = Operations(record)
    operations.menu()