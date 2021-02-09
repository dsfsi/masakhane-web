import { Container } from 'react-bootstrap';
import Navbar from 'react-bootstrap/Navbar'

import TranslateCard from './components/translateCard';

function App() {
  return (
    <Container className="my-4">
      <Navbar bg="primary" variant="dark" expand="lg">
        <Navbar.Brand href="#home">Masakhane</Navbar.Brand>
      </Navbar>
      <br />
      <br />
      <TranslateCard />
      <br />
      <p style={{fontSize: 12, color: 'gray'}}>This is a community research project. Read more about it <span style={{color: 'blue'}}>here</span></p>
    </Container>
  );
}

export default App;
