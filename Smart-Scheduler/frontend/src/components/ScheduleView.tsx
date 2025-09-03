import { useEffect, useState } from "react";
import { getSchedule } from "../api/tasks";

export default function ScheduleView() {
	const [schedule, setSchedule] = useState(null);

	useEffect(() => {
		getSchedule().then(setSchedule);
	}, []);

	return (
		<div className="p-4 border rounded-xl shadow-md">
			<h2 className="text-xl font-bold">Schedule</h2>
			{schedule ? (
				<pre className="mt-2">{JSON.stringify(schedule, null, 2)}</pre>
			) : (
				<p>Loading...</p>
			)}
		</div>
	);
}
