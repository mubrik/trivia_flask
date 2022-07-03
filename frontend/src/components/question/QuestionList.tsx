import * as React from 'react';
// material
import {
  Stack,
  Container, Divider
} from '@mui/material/';
// types
import { 
  IPaginationState 
} from '../../types/customTypes';
import { 
  IServerQuestion,
  IServerCategory
} from '../../types/serverDataTypes';

interface IComponentProps {
  questions: IServerQuestion[]
  setPaginationData: React.Dispatch<React.SetStateAction<IPaginationState>>;
  setCategories: React.Dispatch<React.SetStateAction<IServerCategory[]>>;
  setQuestions: React.Dispatch<React.SetStateAction<IServerQuestion[]>>;
}

const QuestionList = () => {

  return(
    <>
    </>
  );
};