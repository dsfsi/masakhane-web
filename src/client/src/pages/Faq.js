import { Container, Card } from 'react-bootstrap'

export default function FAQPage() {
    return(
        <div>
            <Container className="my-4">
                <Card style={{ width: '100%' }}>
                    <Card.Body>
                        <Card.Title>FAQ</Card.Title>
                        <Card.Subtitle className="mb-2 text-muted">Enter  subtitle here</Card.Subtitle>
                        <div>
                            <Card.Text style={{ fontSize: 14, color: 'gray' }}>
                                Faqs go here...
                            </Card.Text>
                        </div>
                        <br />
                    </Card.Body>
                </Card>
            </Container>
        </div>
    )
}