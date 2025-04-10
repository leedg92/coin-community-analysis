import { NextRequest, NextResponse } from 'next/server';

interface Message {
  id: number;
  message: string;
  source: string;
  created_at: string;
}

interface BackendResponse {
  id?: number;
  message?: string;
  content?: string;
  created_at?: string;
  createdAt?: string;
}

export async function GET(request: NextRequest) {
  console.log('=== BFF API Route ===');
  const { searchParams } = new URL(request.url);
  const source = searchParams.get('source');
  
  console.log('Request URL:', request.url);
  console.log('Source param:', source);

  if (!source) {
    return NextResponse.json({ error: 'Source parameter is required' }, { status: 400 });
  }

  let baseUrl = '';
  let endpoint = '';

  if (source === 'java') {
    baseUrl = 'http://localhost:8082';
    endpoint = '/api/test/java';
  } else if (source === 'node') {
    baseUrl = 'http://localhost:3001';
    endpoint = '/api/test/node';
  } else {
    return NextResponse.json({ error: 'Invalid source' }, { status: 400 });
  }

  const url = `${baseUrl}${endpoint}`;
  console.log('Will call:', url);

  try {
    const response = await fetch(url);
    console.log('Response status:', response.status);

    if (!response.ok) {
      // 에러 응답을 프론트엔드에 맞게 변환
      return NextResponse.json([], { status: 200 }); // 에러 시 빈 배열 반환
    }

    const data = await response.json();
    
    // 백엔드 응답을 프론트엔드에 맞는 형식으로 변환
    const formattedData: Message[] = Array.isArray(data) ? data.map((item: BackendResponse) => ({
      id: item.id || 0,
      message: item.message || item.content || '내용 없음',
      source: source,
      created_at: item.created_at || item.createdAt || new Date().toISOString()
    })) : [];

    return NextResponse.json(formattedData);
  } catch (error) {
    console.error('Error fetching data:', error);
    return NextResponse.json([], { status: 200 }); // 에러 시 빈 배열 반환
  }
} 