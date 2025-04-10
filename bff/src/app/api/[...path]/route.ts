import { NextRequest, NextResponse } from 'next/server';

const BACKEND_URLS = {
  java: 'http://localhost:8080',
  node: 'http://localhost:3001'
};

export async function GET(request: NextRequest) {
  const path = request.nextUrl.pathname;
  
  // /api/java/* 또는 /api/node/* 경로 확인
  const match = path.match(/^\/api\/(java|node)\/(.*)/);
  if (!match) {
    return NextResponse.json({ error: 'Invalid API path' }, { status: 400 });
  }

  const [, backendType, backendPath] = match;
  const backendUrl = `${BACKEND_URLS[backendType as keyof typeof BACKEND_URLS]}/${backendPath}`;

  try {
    const response = await fetch(backendUrl, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`Backend ${backendType} returned ${response.status}`);
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error(`Error proxying to ${backendType} backend:`, error);
    return NextResponse.json(
      { error: `Failed to connect to ${backendType} backend` },
      { status: 502 }
    );
  }
}

export async function POST(request: NextRequest) {
  const path = request.nextUrl.pathname;
  
  // /api/java/* 또는 /api/node/* 경로 확인
  const match = path.match(/^\/api\/(java|node)\/(.*)/);
  if (!match) {
    return NextResponse.json({ error: 'Invalid API path' }, { status: 400 });
  }

  const [, backendType, backendPath] = match;
  const backendUrl = `${BACKEND_URLS[backendType as keyof typeof BACKEND_URLS]}/${backendPath}`;

  try {
    const body = await request.json();
    const response = await fetch(backendUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      throw new Error(`Backend ${backendType} returned ${response.status}`);
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error(`Error proxying to ${backendType} backend:`, error);
    return NextResponse.json(
      { error: `Failed to connect to ${backendType} backend` },
      { status: 502 }
    );
  }
} 