'use client';

import { useEffect, useState } from 'react';
import { getBuildings } from '@/lib/api';
import { Building } from '@/lib/types';
import Link from 'next/link';
import { Building2, MapPin, Users, Layers, Search } from 'lucide-react';

export default function BuildingsPage() {
  const [buildings, setBuildings] = useState<Building[]>([]);
  const [campusFilter, setCampusFilter] = useState<'all' | 'south' | 'north'>('all');
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const data = await getBuildings();
        setBuildings(data);
      } catch (err) {
        console.error('Failed to load buildings', err);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  const filtered = buildings.filter(b => {
    const matchesCampus = campusFilter === 'all' || b.campus === campusFilter;
    const matchesSearch = b.name.toLowerCase().includes(search.toLowerCase()) || 
                          b.code.toLowerCase().includes(search.toLowerCase()) ||
                          b.type.toLowerCase().includes(search.toLowerCase());
    return matchesCampus && matchesSearch;
  });

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-gray-800">Campus Buildings</h1>
          <p className="text-gray-500 text-sm mt-1">Boğaziçi University Güney & Kuzey Campus Facilities (21 Buildings)</p>
        </div>

        {/* Filter Controls */}
        <div className="flex flex-wrap items-center gap-3">
          <div className="relative">
            <Search className="absolute left-3 top-2.5 text-gray-400" size={16} />
            <input 
              type="text" 
              placeholder="Search building..." 
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="pl-9 pr-4 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary w-48 md:w-64"
            />
          </div>

          <div className="bg-gray-100 p-1 rounded-lg flex text-sm">
            <button 
              onClick={() => setCampusFilter('all')} 
              className={`px-3 py-1.5 rounded-md transition ${campusFilter === 'all' ? 'bg-white shadow-sm font-medium text-gray-800' : 'text-gray-500'}`}
            >
              All ({buildings.length})
            </button>
            <button 
              onClick={() => setCampusFilter('south')} 
              className={`px-3 py-1.5 rounded-md transition ${campusFilter === 'south' ? 'bg-white shadow-sm font-medium text-gray-800' : 'text-gray-500'}`}
            >
              Güney
            </button>
            <button 
              onClick={() => setCampusFilter('north')} 
              className={`px-3 py-1.5 rounded-md transition ${campusFilter === 'north' ? 'bg-white shadow-sm font-medium text-gray-800' : 'text-gray-500'}`}
            >
              Kuzey
            </button>
          </div>
        </div>
      </div>

      {loading ? (
        <div className="h-64 flex items-center justify-center text-gray-400">Loading buildings...</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filtered.map(b => (
            <Link 
              key={b.id} 
              href={`/buildings/${b.id}`}
              className="bg-white border border-gray-200 rounded-xl p-5 hover:shadow-md transition group block"
            >
              <div className="flex items-start justify-between">
                <div className="bg-emerald-50 text-emerald-700 p-2.5 rounded-lg group-hover:bg-emerald-600 group-hover:text-white transition">
                  <Building2 size={24} />
                </div>
                <span className="text-xs font-semibold px-2.5 py-1 rounded-full bg-gray-100 text-gray-600">
                  {b.code}
                </span>
              </div>

              <h2 className="text-lg font-bold text-gray-800 mt-4 group-hover:text-emerald-700 transition">
                {b.name}
              </h2>
              
              <div className="flex items-center text-xs text-gray-500 mt-1 space-x-2">
                <span className="flex items-center"><MapPin size={12} className="mr-0.5" /> {b.campus === 'south' ? 'Güney Kampüs' : 'Kuzey Kampüs'}</span>
                <span>•</span>
                <span>{b.type}</span>
              </div>

              <div className="grid grid-cols-2 gap-2 mt-4 pt-4 border-t border-gray-100 text-xs text-gray-600">
                <div className="flex items-center">
                  <Users size={14} className="mr-1.5 text-gray-400" />
                  Capacity: <span className="font-semibold ml-1">{b.total_capacity}</span>
                </div>
                <div className="flex items-center">
                  <Layers size={14} className="mr-1.5 text-gray-400" />
                  Floors: <span className="font-semibold ml-1">{b.floors}</span>
                </div>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
