 from time import time
 from unittest import IsolatedAsyncioTestCase, main
 from unittest.mock import patch

 from gateway.average_calculator import AverageCalculator
 from gateway.channel import Channel
 from gateway.environment import Environment


 @patch.dict('os.environ', {
 	'CHANNEL_MAX_FRAMES_PER_SECOND': '13',
 	'INTERVALS': '1 15 85',


 async def test_calculate_averages_no_values(self) -> None:
 	# TODO: Check that value was not inserted in database.
 	channel = Channel('reduce', 3)
 	average_calculator = AverageCalculator(channel, self.__environment)
 	channel = Channel('reduce', 3)
 	average_calculator = AverageCalculator(channel, self.__environment)

 	await average_calculator.calculate_average()

 async def test_calculate_averages_old_timestamp(self) -> None:
 	# TODO: Check that value was not inserted in database.
 	channel = Channel('glory', 0)
 	average_calculator = AverageCalculator(channel, self.__environment)
 	average_calculator.add_value(0.1699, time() - 1000000)
 	average_calculator.add_value(1.759, time() - 1000000)
 	channel = Channel('glory', 0)
 	average_calculator = AverageCalculator(channel, self.__environment)
 	average_calculator.add_value(0.1699, time() - 1000000)
 	average_calculator.add_value(1.759, time() - 1000000)

 	await average_calculator.calculate_average()

 async def test_calculate_averages_future_timestamp(self) -> None:
 	# TODO: Check that value was not inserted in database.
 	channel = Channel('construct', 5)
 	calculator = AverageCalculator(channel, self.__environment)
 	calculator.add_value(1.7701, time() + 1000000)
 	channel = Channel('construct', 5)
 	calculator = AverageCalculator(channel, self.__environment)
 	calculator.add_value(1.7701, time() + 1000000)

 	await calculator.calculate_average()
 	await calculator.calculate_average()

 async def test_calculate_averages_old_timestamp_in_non_strict_mode(self) -> None:
 	# TODO: Check that value was inserted in database.
 	pass


 if __name__ == '__main__':
 	main()