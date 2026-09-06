import { NextResponse } from 'next/server';

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const scenarioType = body.scenario_type || 'heatwave';
    const params = body.params || {};

    let energyDelta = 0;
    let occDelta = 0;
    let foodDelta = 0;
    const insights: string[] = [];

    if (scenarioType === 'heatwave') {
      const temp = params.temperature || 38;
      energyDelta = Math.round((temp - 22) * 4.2);
      occDelta = -12;
      foodDelta = -8;
      insights.push(`Extreme heatwave (${temp}°C): HVAC cooling load spikes by +${energyDelta}%. Outdoor transit shifts to air-conditioned halls.`);
    } else if (scenarioType === 'exam_week') {
      occDelta = 35;
      energyDelta = 22;
      foodDelta = 25;
      insights.push('Midterm & Final exams: Campus attendance surges by +35%. Aptullah Kuran Library operating at 100% capacity 24/7.');
    } else if (scenarioType === 'event') {
      occDelta = 25;
      energyDelta = 18;
      foodDelta = 30;
      insights.push('Major Campus Festival / Conference: +1,000 visitors at Albert Long Hall and South Square.');
    } else if (scenarioType === 'rain') {
      occDelta = 10;
      energyDelta = 8;
      foodDelta = 15;
      insights.push('Heavy Istanbul rain: Students remain indoors; cafeteria and canteen loads increase by +15%.');
    } else if (scenarioType === 'building_closure') {
      occDelta = -15;
      energyDelta = -28;
      insights.push('Temporary building maintenance: Occupants redistributed to adjacent faculty blocks.');
    } else {
      occDelta = -60;
      energyDelta = -55;
      foodDelta = -70;
      insights.push('Summer term: Low campus footprint; consolidation to North Campus recommended.');
    }

    const comparisons = [
      {
        metric: 'Campus Energy Demand',
        baseline_value: 11.4,
        scenario_value: Math.round((11.4 * (1 + energyDelta / 100)) * 10) / 10,
        diff: Math.round((11.4 * (energyDelta / 100)) * 10) / 10,
        diff_percent: energyDelta
      },
      {
        metric: 'Cafeteria Meal Preparation',
        baseline_value: 3580,
        scenario_value: Math.round(3580 * (1 + foodDelta / 100)),
        diff: Math.round(3580 * (foodDelta / 100)),
        diff_percent: foodDelta
      },
      {
        metric: 'Peak Campus Population',
        baseline_value: 6250,
        scenario_value: Math.round(6250 * (1 + occDelta / 100)),
        diff: Math.round(6250 * (occDelta / 100)),
        diff_percent: occDelta
      }
    ];

    return NextResponse.json({
      scenario_type: scenarioType,
      comparisons: comparisons,
      insights: insights
    });
  } catch (e) {
    return NextResponse.json({ error: 'Failed to simulate scenario' }, { status: 400 });
  }
}
