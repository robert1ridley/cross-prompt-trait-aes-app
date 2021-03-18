import React, { useEffect } from "react";
import Chart from "chart.js";

export default function RadarChart(props) {
	useEffect(() => {
		const ctx = document.getElementById("myChart");
		new Chart(ctx, {
			type: "radar",
			data: {
				labels: props.data.labels,
				datasets: [
					{
						label: "Scores",
						data: props.data.scores,
						borderColor: '#3f51b5',
						borderWidth: 1
					}
				]
			},
			options: {
				scale: {
						angleLines: {
								display: true
						},
						ticks: {
								suggestedMin: 0,
								suggestedMax: 100
						}
				}
			}
		});
	});
	return (
		<div>
			<canvas id="myChart" width="100%" height="100%" style={{paddingBottom: 20}} />
		</div>
	);
}