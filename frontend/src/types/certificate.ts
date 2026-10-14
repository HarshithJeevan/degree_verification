export type VerificationStatusType = 'verified' | 'requires_review' | 'pending' | 'rejected' | '';
export type FieldMatchStatus = 'match' | 'mismatch' | 'review' | '';                         // remove all (| '') afterwards to the end
export type MatchType = 'exact' | 'fuzzy' | 'vocabulary' | 'coordinate' | '';
export type LayoutStatus = 'match' | 'position_difference' | 'anomaly' | '';

export interface CertificateField {
  name?: string;
  expectedValue?: string;
  extractedValue?: string;
  matchStatus?: FieldMatchStatus;
  confidence?: number;
  matchType?: MatchType;
  reason?: string;
}

export interface LayoutRegion {
  name?: string;
  status?: LayoutStatus;
  expectedPosition?: { x: number; y: number; w: number; h: number };
  actualPosition?: { x: number; y: number; w: number; h: number };
  deviation?: number;            //?
}

export interface StudentRecord {
  rollNumber?: string;
  englishName?: string;
  hindiName?: string;
  degree?: string;
  branch?: string;
  dateOfIssue?: string;
  cgpa?: string;
  convocationNumber?: string;
}

export interface Certificate {
  id?: string;
  fileName?: string;
  fileSize?: string;
  fileType?: string;
  uploadTime?: string;
  studentRecord?: StudentRecord;
  fields?: CertificateField[];
  layoutRegions?: LayoutRegion[];
  overallConfidence?: number;
  status?: VerificationStatusType;
  reviewReason?: string;              //?
}
