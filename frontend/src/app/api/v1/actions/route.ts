import { NextResponse } from 'next/server';

export async function GET() {
  const actions = [
    {
      id: 'act-1',
      priority: 'HIGH',
      type: 'food',
      title: 'Lunch Rush Production Target: Etli Nohut Yemeği',
      time: '11:30 - 13:45',
      location: 'Kuzey Yemekhanesi & Piramit',
      description: "Classroom dismissal surge at 12:00. 633 students expected simultaneous. Today's official dish: Etli Nohut Yemeği (317 kcal). Prepare 3,584 portions to prevent queuing and food waste.",
      impact_value: 52,
      impact_unit: 'kg food',
      icon: 'Utensils'
    },
    {
      id: 'act-2',
      priority: 'HIGH',
      type: 'energy',
      title: 'Consolidate Kare Blok (KB) Evening Study Groups',
      time: '18:00 - 22:00',
      location: 'Kare Blok',
      description: 'Real OBIKAS schedule has 0 lectures after 18:00. Consolidate remaining students into Floors 1-2. Power down Floors 3-5 HVAC (Outdoor: 21°C).',
      impact_value: 175,
      impact_unit: 'kWh',
      icon: 'Zap'
    },
    {
      id: 'act-3',
      priority: 'MEDIUM',
      type: 'space',
      title: 'Redirect South Campus Lunch Overflow to Orta Kantin',
      time: '12:15 - 13:15',
      location: 'Güney Yemekhanesi & Dodge Hall',
      description: 'Güney Yemekhanesi (159 seats) projected at 96% capacity (152 students). Open auxiliary seating in Orta Kantin (Dodge Hall).',
      impact_value: 75,
      impact_unit: 'students',
      icon: 'Building2'
    },
    {
      id: 'act-4',
      priority: 'MEDIUM',
      type: 'energy',
      title: 'New Hall (NH) Tiered Lecture Hall Eco-Ventilation',
      time: '12:00 - 13:00',
      location: 'Yeni Bina (NH)',
      description: 'Tiered auditoriums NH 101, 201, 301, 401 empty during lunch break. Shift ventilation to eco-mode.',
      impact_value: 90,
      impact_unit: 'kWh',
      icon: 'Zap'
    }
  ];
  return NextResponse.json(actions);
}
