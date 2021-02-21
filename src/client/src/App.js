import { Navbar, Nav, Container, Jumbotron, Image, Row, Col } from 'react-bootstrap'

// // import { Container } from 'react-bootstrap';
// import Navbar from 'react-bootstrap/Navbar'

import TranslateCard from './components/translateCard';
import image from './images/masakhane_bg2.png';

function App() {
  return (
    <div>
      <Navbar style={{ backgroundColor: '#F2F0E9', width: '100%' }} >
        <Navbar.Brand href="#home" variant="dark" style={{ fontFamily: 'lato', color: 'grey'}}>Masakhane</Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav" className="justify-content-start">
          <Nav className="ml-auto">
            <Nav.Link href="#home">Home</Nav.Link>
            <Nav.Link href="https://www.masakhane.io/" target='blank'>About</Nav.Link>
            <Nav.Link href="https://www.masakhane.io/faq" target='blank'>FAQ</Nav.Link>
          </Nav>
        </Navbar.Collapse>
      </Navbar>
      <Jumbotron style={{ backgroundColor: '#F2F0E9', paddingTop: '50px', paddingBottom: '100px', backgroundImage: `url(${image})`,backgroundSize: 'cover', backgroundSize: 'cover'}} fluid>
        <Container>
          <Row style={{display:'flex', justifyContent: 'center', alignItems: 'center'}}>
            <Col>
              <h1 style={{ fontFamily: 'lato, sans-serif', fontSize: 80, display:'flex', justifyContent: 'center',alignItems: 'center'}}>Masakhane</h1>
              <p style={{display:'flex', justifyContent: 'center',alignItems: 'center'}}>Machine Translation Service for African Languages</p>
            </Col>
          </Row>
        </Container>
      </Jumbotron>
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

export default App;
