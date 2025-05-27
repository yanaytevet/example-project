export interface Action {
  display: string;
  icon?: string;
  callback: () => void;
}
