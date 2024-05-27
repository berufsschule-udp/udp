interface TimeFactory {
	now: () => Time;
	ofEmpty: () => Time;
	ofMilliseconds: (milliseconds: number) => Time;
	ofSeconds: (seconds: number) => Time;
	ofDirtySeconds: (...seconds: (Time | number | string | null | undefined)[]) => Time;
	ofMinutes: (minutes: number) => Time;
	ofHours: (hours: number) => Time;
	ofDays: (days: number) => Time;
	ofWeeks: (weeks: number) => Time;
	ofMonths: (months: number) => Time;
}

export interface Time {
	toMilliseconds: () => number;
	toSeconds: () => number;
	toMinutes: () => number;
	toHours: () => number;
	toDays: () => number;
	toWeeks: () => number;
	toMonths: () => number;
	toDate: () => Date;

	toPrettyString: () => string;

	isBefore: (time: Time) => boolean;
	isAfter: (time: Time) => boolean;
	equals: (time: Time) => boolean;

	minus: (time: Time) => Time;
	minusSeconds: (seconds: number) => Time;
	plus: (time: Time) => Time;
	plusSeconds: (seconds: number) => Time;
}

export const Time = Object.freeze({
	now: () => TimeInstance(Date.now() * 1000),
	ofEmpty: () => TimeInstance(0),
	ofMilliseconds: (milliseconds: number) => TimeInstance(milliseconds),
	ofSeconds: (seconds: number) => TimeInstance(seconds * 1000),
	ofDirtySeconds: (...seconds: (Time | number | string | null | undefined)[]) => {
		const value = seconds.find(value => value);

		return TimeInstance(
			typeof value === "number"
				? value
				: typeof value === "string"
					? +value
					: (value as Time).toMilliseconds()
		);
	},
	ofMinutes: (minutes: number) => TimeInstance(minutes * 60000),
	ofHours: (hours: number) => TimeInstance(hours * 3600000),
	ofDays: (days: number) => TimeInstance(days * 86400000),
	ofWeeks: (weeks: number) => TimeInstance(weeks * 604800000),
	ofMonths: (months: number) => TimeInstance(months * 2592000000)
}) as TimeFactory;

function TimeInstance(milliseconds: number) {
	return {
		toMilliseconds: () => milliseconds,
		toSeconds: () => Math.floor(milliseconds / 1000),
		toMinutes: () => Math.floor(milliseconds / 60000),
		toHours: () => Math.floor(milliseconds / 3600000),
		toDays: () => Math.floor(milliseconds / 86400000),
		toWeeks: () => Math.floor(milliseconds / 604800000),
		toMonths: () => Math.floor(milliseconds / 2592000000),
		toDate: () => new Date(Math.floor(milliseconds / 1000)),
		toPrettyString: () =>
			milliseconds < 60000
				? `${milliseconds / 1000}s`
				: milliseconds < 3600000
					? `${Math.floor(milliseconds / 60000)}m ${milliseconds % 60000 / 1000}s`
					: milliseconds < 86400000
						? `${Math.floor(milliseconds / 3600000)}h ${Math.floor((milliseconds % 3600000) / 60000)}m`
						: `${Math.floor(milliseconds / 86400000)}d ${Math.floor((milliseconds % 86400000) / 3600000)}h`,
		isBefore: (time: Time) => milliseconds < time.toMilliseconds(),
		isAfter: (time: Time) => milliseconds > time.toMilliseconds(),
		equals: (time: Time) => milliseconds === time.toMilliseconds(),
		minus: (time: Time) => Time.ofMilliseconds(milliseconds - time.toMilliseconds()),
		minusSeconds: (seconds: number) => Time.ofMilliseconds(milliseconds - seconds * 1000),
		plus: (time: Time) => Time.ofMilliseconds(milliseconds + time.toMilliseconds()),
		plusSeconds: (seconds: number) => Time.ofMilliseconds(milliseconds + seconds * 1000)
	} as Time;
}