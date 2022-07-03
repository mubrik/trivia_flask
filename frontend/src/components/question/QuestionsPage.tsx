import * as React from 'react';
// material
import {
  Grid, Stack,
  Container, Divider
} from '@mui/material/';
// axios
import axios from 'axios';
// notification
import { useSnackbar } from 'notistack';
// types
import { 
  IPaginationState 
} from '../../types/customTypes';
import { 
  IServerQuestionResponse, IServerQuestion,
  IServerCategory
} from '../../types/serverDataTypes';

const initialPaginationState: IPaginationState = {
  page: 1,
  limit: 0,
  total: 0,
};

const QuestionPage = (): JSX.Element => {
  // states
  const [paginationData, setPaginationData] = React.useState<IPaginationState>(initialPaginationState);
  const [categories, setCategories] = React.useState<IServerCategory[]>([]);
  const [questions, setQuestions] = React.useState<IServerQuestion[]>([]);

  // notify
  const { enqueueSnackbar } = useSnackbar();

  // effect to load initial data
  React.useEffect(() => {
    // abort controller 
    const abortController = new AbortController()
    // get page
    axios.get<IServerQuestionResponse>(
        `/api/questions?page=${paginationData.page}`,
        { signal: abortController.signal }
      )
      .then(res => {
        console.log(res.data);
        const {questions, total_questions, categories} = res.data;

        setCategories(categories);
        setQuestions(questions);
        setPaginationData(prevState => ({
          ...prevState,
          total: total_questions
        }));

      })
      .catch(err => {
        console.log(err);
        enqueueSnackbar(err.message, {
          variant: 'error',
          autoHideDuration: 3000,
        })
      });
      // cancel req on unmount
      return () => {
        abortController.abort();
      }
  }, [enqueueSnackbar, paginationData.page]);

  return(
    <Grid container spacing={2}>
      <Grid item sm={0} md={2}>
        <CategorySidebar />
      </Grid>
      <Grid item sm={12} md={10}>

      </Grid>
    </Grid>
  );
};

const CategorySidebar = () => {

  return(
    <Container maxWidth={"xl"}>
      <h3> Categories </h3>
      <Stack
        direction="column"
        justifyContent="flex-start"
        alignItems="flex-start"
        spacing={1}
        divider={<Divider orientation="horizontal" flexItem />}
      >
      </Stack>
    </Container>
  );
};