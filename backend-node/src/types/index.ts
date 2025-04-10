export interface Message {
  id: number;
  content: string;
  source: string;
  created_at: Date;
}

export interface CommunityData {
  id: number;
  platform: string;
  content: string;
  sentiment_score: number;
  created_at: Date;
} 