export interface IServerQuestion {
  id: number;
  question: string;
  answer: string;
  category: number;
  difficulty: number;
}

export interface IServerCategory {
  id: number;
  type: string;
}

export interface IServerCategoryResponse {
  categories: IServerCategory[];
  total_categories: number;
}

export interface IServerQuestionResponse {
  questions: IServerQuestion[];
  categories: IServerCategory[];
  total_questions: number;
}
