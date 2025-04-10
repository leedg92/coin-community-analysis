import { NextResponse } from 'next/server';
import { config } from '@coin-community/config';

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const source = searchParams.get('source');
  
  try {
    let baseUrl;
    if (source === 'java') {
      baseUrl = `${config.urls.javaBackend}/api/messages`;  // Java 백엔드의 메시지 API
    } else if (source === 'node') {
      baseUrl = `${config.urls.nodeBackend}/test`;  // Node.js 백엔드의 메시지 API
    } else {
      return NextResponse.json(
        { error: 'Invalid source parameter' },
        { status: 400 }
      );
    }

    const response = await fetch(baseUrl);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('Error:', error);
    return NextResponse.json(
      { error: 'Failed to fetch data' },
      { status: 500 }
    );
  }
} 