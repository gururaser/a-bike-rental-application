# a-bike-rental-application
 A bike rental application with SQLite

## Getting Started
Adapted as a Python console application with the "Bike Shop" theme of the product purchase - rental system logic.

## Features
- Buying or renting bikes within stock
- Payment system that displays the number of banknotes you need to complete the payment.

  - Like this, ( (You can pay with 100 banknotes)
    How many 100 TRY ?: )
- Ability to view order history in detail
- Ability to return product

## Security
This is how SQL queries were written to avoid SQL Injection.



```python
self.cursor.execute(f"UPDATE {table_name} SET {info_name} = {new_value} WHERE id = ?", (info_id,))
```

## How to use

### To buy bike
- Firstly, Enter '1' to reach 'Buy Bike' section
- Then enter ID of bike that you want to buy
- Follow the necessary steps

## To rent bike
- Firstly, Enter '2' to reach 'Rent Bike' section
- Then enter ID of bike that you want to rent
- Choose that what kind of hire you want ( Hourly or Daily )
- Follow the necessary steps

## To return bike
- Firstly, Enter '3' to reach 'Show My Order History' section
- Then enter ID of order that you want to return
- Enter '1' if you want to return a bike that you bought
- Enter '2' if you want to return a bike that you rented
- Follow the necessary steps


## Screenshots

![Screenshot 1](https://github.com/gururaser/a-bike-rental-application/blob/main/A%20Bike%20Rental%20System%20with%20SQLite/screenshot1.png)
![Screenshot 1](https://github.com/gururaser/a-bike-rental-application/blob/main/A%20Bike%20Rental%20System%20with%20SQLite/screenshot2.png)
![Screenshot 1](https://github.com/gururaser/a-bike-rental-application/blob/main/A%20Bike%20Rental%20System%20with%20SQLite/screenshot3.png)
