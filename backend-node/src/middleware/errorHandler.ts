import { Request, Response, NextFunction } from 'express';

export interface CustomError extends Error {
  status?: number;
}

export const errorHandler = (
  err: CustomError,
  req: Request,
  res: Response,
  next: NextFunction
) => {
  console.error('에러 발생:', err);

  const status = err.status || 500;
  const message = err.message || '서버 내부 오류가 발생했습니다';

  res.status(status).json({
    error: {
      status,
      message,
    },
  });
}; 