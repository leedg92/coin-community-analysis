'use client';

import { useState } from 'react';

interface Message {
  id: number;
  message: string;
  source: string;
  created_at: string;
}

export default function Home() {
  const [nodeMessages, setNodeMessages] = useState<Message[]>([]);
  const [javaMessages, setJavaMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState<{[key: string]: boolean}>({});

  const fetchMessages = async (source: 'node' | 'java') => {
    try {
      setLoading(prev => ({ ...prev, [source]: true }));
      const response = await fetch(`http://localhost:3000/api/${source}/test`);
      const data = await response.json();
      if (source === 'node') {
        setNodeMessages(data);
      } else {
        setJavaMessages(data);
      }
    } catch (error) {
      console.error(`Error fetching ${source} messages:`, error);
    } finally {
      setLoading(prev => ({ ...prev, [source]: false }));
    }
  };

  return (
    <main className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800">
      <div className="container mx-auto px-4 py-12">
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold mb-4 bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-green-600 dark:from-blue-400 dark:to-green-400">
            코인 커뮤니티 분석 플랫폼
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-300 mb-8">
            실시간으로 코인 커뮤니티의 동향을 분석하고 인사이트를 제공합니다
          </p>
          <div className="flex justify-center gap-4 mb-12">
            <button
              onClick={() => fetchMessages('node')}
              className="px-6 py-3 bg-gradient-to-r from-blue-500 to-blue-600 text-white rounded-lg shadow-lg hover:shadow-xl transition-all duration-200 flex items-center space-x-2 disabled:opacity-50 hover:scale-105"
              disabled={loading.node}
            >
              {loading.node ? (
                <span className="inline-block animate-spin mr-2">⌛</span>
              ) : (
                <span className="inline-block mr-2">📊</span>
              )}
              Node 데이터 조회
            </button>
            <button
              onClick={() => fetchMessages('java')}
              className="px-6 py-3 bg-gradient-to-r from-green-500 to-green-600 text-white rounded-lg shadow-lg hover:shadow-xl transition-all duration-200 flex items-center space-x-2 disabled:opacity-50 hover:scale-105"
              disabled={loading.java}
            >
              {loading.java ? (
                <span className="inline-block animate-spin mr-2">⌛</span>
              ) : (
                <span className="inline-block mr-2">📈</span>
              )}
              Java 데이터 조회
            </button>
          </div>
        </div>

        <div className="grid md:grid-cols-2 gap-8 max-w-6xl mx-auto">
          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6 transition-all duration-200 hover:shadow-xl border border-gray-100 dark:border-gray-700">
            <h2 className="text-2xl font-bold mb-4 text-blue-600 dark:text-blue-400 flex items-center">
              <span className="inline-block mr-2">🔷</span>
              Node 메시지
            </h2>
            <div className="space-y-4">
              {nodeMessages.length === 0 ? (
                <p className="text-gray-500 dark:text-gray-400 text-center py-4">메시지가 없습니다</p>
              ) : (
                nodeMessages.map((msg) => (
                  <div key={msg.id} className="border-l-4 border-blue-500 pl-4 py-2 bg-gray-50 dark:bg-gray-700 rounded">
                    <p className="text-gray-800 dark:text-gray-200">{msg.message}</p>
                    <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
                      {new Date(msg.created_at).toLocaleString()}
                    </p>
                  </div>
                ))
              )}
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6 transition-all duration-200 hover:shadow-xl border border-gray-100 dark:border-gray-700">
            <h2 className="text-2xl font-bold mb-4 text-green-600 dark:text-green-400 flex items-center">
              <span className="inline-block mr-2">🔷</span>
              Java 메시지
            </h2>
            <div className="space-y-4">
              {javaMessages.length === 0 ? (
                <p className="text-gray-500 dark:text-gray-400 text-center py-4">메시지가 없습니다</p>
              ) : (
                javaMessages.map((msg) => (
                  <div key={msg.id} className="border-l-4 border-green-500 pl-4 py-2 bg-gray-50 dark:bg-gray-700 rounded">
                    <p className="text-gray-800 dark:text-gray-200">{msg.message}</p>
                    <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
                      {new Date(msg.created_at).toLocaleString()}
                    </p>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
