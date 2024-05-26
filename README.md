# Tire management
#### Video Demo:  <[URL HERE](https://youtu.be/Vx5-VTUFEcg)>
- Autor: Ninh Vo
- GitHub: DucNinhVo
- edX usernames; ninhvo
- Location: Sìegen, Germany
- Recorded Date: 11/04/2024
### Introduction
If you are a fan of car racing and specially 24hr GT Racing, maybe you would have known that managing tires efficiently is crucial during these endurance races, especially with changing weather conditions. With only one car but four drivers in a 24-hour race, tire adjustments are critical for performance. In high-stakes motorsport, even minor details in tire management can make the difference between victory and defeat.
This project was developed to support the above purpose.
> Die Land-Motorsport GmbH from Niederdreisbach in the Westerwald region offers valuable insights into the intricacies of tire management

### 1. Process
- Audi provides its racing teams with a set number of tires for each 24-hour race, with allocation managed on-site by Michelin, the tire partner. Michelin operates a central warehouse where teams, like Team Land, retrieve their tire sets.
- An engineer calculates the required tires and informs Team Land's tire manager. An employee then orders the tires from Michelin along with the rims, receiving an estimate for tire assembly time.
- Upon return, the tire manager sets a timer. Once elapsed, an employee collects the tires. If delayed, the manager adjusts the collection schedule.
- After labeling the tires, the manager or an employee adjusts the tire pressure individually based on the engineer's calculations. The tires are then heated with electric blankets, typically set at 90 or 40 degrees, for approximately 1.5 hours.
- As the vehicle nears the pit stop, the tires are transported for assembly. The old set is exchanged, and specifications for the new set are provided to Michelin.
- Employees monitor external and route temperatures every 30 minutes, recording them. Telemetry data from the car aids the engineer and manager in determining adjustments for the next tire set, such as air pressure changes or tire type.
- All data, including tire adjustments and temperature readings, is logged in an Excel sheet for process documentation and review.

### 2. Features
The web application should streamline the tire management process by enabling simultaneous collaboration among engineers, tire managers, and employees on a shared dataset. Key features include:

- Real-time Collaboration: Multiple users can work on the same dataset concurrently, ensuring seamless coordination.
- Basic Settings Management: Engineers and managers can set parameters such as tire quotas directly within the application.
- Overview: The manager has a comprehensive view of the current status of tire processing, including which tires are being handled.
- Reminder Functionality: Managers and employees receive reminders to pick up tires, with logging of the date and time for accountability.
- Temperature Monitoring: Employees can input temperature readings and receive reminders for 30-minute intervals, ensuring accurate data collection.
- Efficient Data Entry: The application simplifies and accelerates the input and management of values, enhancing overall efficiency.
- Visualization Tools: Users can generate diagrams, such as temperature curves.
- Statistical Analysis: The application provides statistics based on historical data, such as tire usage frequency and types, aiding in decision-making.
- Fuel Quantity Logging: Logging of fuel quantities is included to track fuel consumption and usage patterns.
