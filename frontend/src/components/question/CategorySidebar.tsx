import * as React from 'react';
// material
import {
  Stack,
  Container, Divider
} from '@mui/material/';
// types
import { 
  IServerQuestion,
  IServerCategory
} from '../../types/serverDataTypes';

interface IComponentProps {
  categories: IServerCategory[];
  setQuestions: React.Dispatch<React.SetStateAction<IServerQuestion[]>>;
}

const CategorySidebar = ({
  categories, setQuestions
}: IComponentProps
) => {

  // states
  const [selectedCats, setSelectedCats] = React.useState([]);

  
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

export default CategorySidebar;