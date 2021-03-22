import { Navbar, Nav, Container, Jumbotron, Image, Row, Col } from 'react-bootstrap'

import TranslateCard from '../components/translateCard';
import image from '../images/masakhane-border.png';

function Home() {
  return (
    <div>
      <Container className="my-4">
        
        <br />
        <br />
        <TranslateCard />
        <br />
        <p style={{fontSize: 12, color: 'gray'}}>This is a community research project. Read more about it <span style={{color: 'blue'}}>here</span></p>
      </Container>
    </div>
  );
}

export default Home;
