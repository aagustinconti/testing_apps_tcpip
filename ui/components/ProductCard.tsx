import { IProduct } from "@/utils/interfaces";
import { ActionIcon, Badge, Card, Group, Image, NumberFormatter, Text, Tooltip, rem } from "@mantine/core";

import classes from './ProductCard.module.css'
import { IconEdit, IconTrash } from "@tabler/icons-react";
import ProductDataModal from "./ProductDataModal";
import { useDisclosure } from "@mantine/hooks";
import { useState } from "react";
import { useRouter } from "next/router";
import ProductRemoveModal from "./ProductRemoveModal";

export function ProductCard(props: {
    product: IProduct,
    edit?: boolean,
    delete?: boolean
}) {

    const router = useRouter()

    const [editOpened, editControl] = useDisclosure(false);
    const [removeOpened, removeControl] = useDisclosure(false);

    const [loading, setLoading] = useState(false)

    const onSubmit = async (value: {
        name: string,
        code: string,
        price: number,
        amount: number,
        description: string,
        image: string,
    }) => {

        setLoading(true)

        if (value.image && value.image.length) {

            const imgRes = await fetch('/api/image/add', {
                method: 'post',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ image_base64: value.image })
            })

            if (imgRes.status === 201) {
                value.image = await imgRes.json();
            } else {
                value.image = ''
            }
        }

        const res = await fetch('/api/product/update', {
            method: 'post',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(value)
        })

        if (res.status === 201) return router.reload()

        setLoading(false)
        console.log(res)
        console.log(await res.json())
    }

    return (
        <>
            <ProductDataModal title="Editar producto" buttonText="Guardar" opened={editOpened} close={editControl.close} onSubmit={onSubmit} loading={loading} values={props.product} />
            <ProductRemoveModal opened={removeOpened} close={removeControl.close} name={props.product.name} code={props.product.product_code} />
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

                {(props.delete || props.edit) && (
                    <Card.Section className={classes.section}>
                        <Group justify="flex-end">

                            {props.edit && (
                                <Tooltip label="Editar">
                                    <ActionIcon variant="light" size="lg" aria-label="Editar" onClick={editControl.open}>
                                        <IconEdit style={{ width: rem(20) }} stroke={1.5} />
                                    </ActionIcon>
                                </Tooltip>
                            )}

                            {props.delete && (
                                <Tooltip label="Borrar">
                                    <ActionIcon variant="light" size="lg" aria-label="Borrar" color='red' onClick={removeControl.open}>
                                        <IconTrash style={{ width: rem(20) }} stroke={1.5} />
                                    </ActionIcon>
                                </Tooltip>
                            )}

                        </Group>
                    </Card.Section>
                )}


            </Card >
        </>
    )

}