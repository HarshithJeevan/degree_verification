import { VerificationStatusType } from '../types';

export interface DashboardStats {
  totalCertificates?: number;
  verified?: number;
  requiresReview?: number;
  pending?: number;
}

export interface RecentVerification {
  id?: string;
  studentName?: string;
  rollNumber?: string;
  degree?: string;
  status?: VerificationStatusType;
  confidence?: number;
  date?: string;
}

export const mockDashboardStats: DashboardStats = {};

export const mockRecentVerifications: RecentVerification[] = [];
