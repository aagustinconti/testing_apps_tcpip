import { IProduct } from "@/utils/interfaces";
import { Badge, Card, Group, Image, NumberFormatter, Text } from "@mantine/core";

export function ProductCard(props: { product: IProduct }) {

    return (
        <Card
            shadow="sm"
            padding="xl"
            radius="md"
            withBorder
        >
            <Card.Section>
                <Image
                    src={props.product.image}
                    fit="cover"
                    alt={props.product.name}
                    fallbackSrc='https://www.theironclinic.com/ironc/wp/wp-content/uploads/2018/08/placeholder-600x400.png'
                    h={300}
                />
            </Card.Section>

            <Group justify="space-between" mt="md" mb="xs">
                <Text fw={500} size="lg">
                    {props.product.name}
                </Text>
                <Badge variant="light" color="gray"># {props.product.product_code}</Badge>
            </Group>

            <Text mb="xs" c="dimmed" size="sm">
                {props.product.description != null && props.product.description.length ? props.product.description : 'Sin descripcion'}
            </Text>

            <Group justify="space-between">
                <Text>
                    Precio:
                </Text>
                <NumberFormatter prefix="$ " value={props.product.price} thousandSeparator="." decimalSeparator="," />
            </Group>
            <Group justify="space-between">
                <Text>
                    Cantidad:
                </Text>
                <NumberFormatter value={props.product.amount} thousandSeparator="." decimalSeparator="," suffix=' unidades' />
            </Group>
        </Card>
    )

}