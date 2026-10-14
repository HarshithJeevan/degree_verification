import type { CertificateField, VerificationStatusType } from './certificate';

export type ReviewDecision = 'approve' | 'reject' | 'further_review' | '';                         // remove all (| '') afterwards to the end

export interface ReviewItem {
  certificateId?: string;
  studentName?: string;
  rollNumber?: string;
  degree?: string;
  flaggedFields?: CertificateField[];
  overallConfidence?: number;
  reviewReason?: string;
  submittedAt?: string;
  status?: VerificationStatusType;
}

export interface ReviewAction {
  decision?: ReviewDecision;
  notes?: string;
  reviewedBy?: string;         //?
  reviewedAt?: string;            //?
}
