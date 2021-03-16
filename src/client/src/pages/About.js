import { Container, Card } from 'react-bootstrap'

export default function About() {
    return(
        <div>
            <Container className="my-4">
                <Card style={{ width: '100%' }}>
                    <Card.Body>
                        <Card.Title>Our Mission</Card.Title>
                        <Card.Subtitle className="mb-2 text-muted">Enter  subtitle here</Card.Subtitle>
                        <div>
                            <Card.Text style={{ fontSize: 12, color: 'gray' }}>
                            Masakhane is a grassroots organisation whose mission is to strengthen and spur NLP research in African languages, for Africans, by Africans. Despite the fact that 2000 of the world’s languages are African, African languages are barely represented in technology. The tragic past of colonialism has been devastating for African languages in terms of their support, preservation and integration. This has resulted in technological space that does not understand our names, our cultures, our places, our history. 

                            Masakhane roughly translates to “We build together” in isiZulu. Our goal is for Africans to shape and own these technological advances towards human dignity, well-being and equity, through inclusive community building, open participatory research and multidisciplinarity. 
                            </Card.Text>
                        </div>
                        <br />
                    </Card.Body>
                </Card>
            </Container>
        </div>
    )
}