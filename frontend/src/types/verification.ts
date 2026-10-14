export type StepStatus = 'pending' | 'processing' | 'completed' | 'warning' | 'error' | '';       // remove all (| '') afterwards to the end

export interface VerificationStep {
  id?: number;
  name?: string;
  description?: string;
  status?: StepStatus;
  detail?: string;                 //?
}

export interface VerificationPipeline {
  certificateId?: string;
  steps?: VerificationStep[];
  currentStep?: number;
  isComplete?: boolean;
}
