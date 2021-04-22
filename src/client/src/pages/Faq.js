import { Container, Card } from 'react-bootstrap'

export default function FAQPage() {
    return(
        <div>
            <Container className="my-4">
                <Card style={{ width: '100%' }}>
                    <Card.Body>
                        <Card.Title>FAQ</Card.Title>
                        {/* <Card.Subtitle className="mb-2 text-muted">Enter  subtitle here</Card.Subtitle> */}
                        <div>
                            <Card.Text style={{ fontSize: 16, color: 'black' }}>
                            1. I was not happy with the translation I got from the service.
                            </Card.Text>
                        </div>
                        <br />
                        <div>
                            <Card.Text style={{ fontSize: 14, color: 'grey' }}>
                            Thank you for trying this service. The Masakhane NLP Translation project built the models used to do the translation. 
                            This website provides a way for us to be able to test how well these models work. This service is still a work in progress and we expect the models to be improved every few months as we get more feedback from users such as yourself. 
                            Please do provide feedback by writing where there is a mistake in the translation so we can provide this information to the researchers. 
                            As such, this service is not a production system (should not be used for official translations).
                            </Card.Text>
                        </div>
                        <br />
                    </Card.Body>
                </Card>
            </Container>
        </div>
    )
}