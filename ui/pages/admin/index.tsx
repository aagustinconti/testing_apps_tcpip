
import cookie from "cookie";
import { useRouter } from 'next/router';
import { TOKEN_NAME } from '@/utils/constants';
import { Navbar } from "@/components/Navbar";
import { ProductCard } from "@/components/ProductCard";
import { IProduct } from "@/utils/interfaces";
import { Card, Grid, Text, Image, Group, Badge, NumberFormatter, Button, Modal, Paper, Title, Stack, TextInput, PasswordInput, FileButton, Avatar, NumberInput, Textarea } from "@mantine/core";
import { useEffect, useRef, useState } from "react";
import { useDisclosure } from "@mantine/hooks";
import { useForm } from "@mantine/form";
import { IconFile } from "@tabler/icons-react";
import ProductModalData from "@/components/ProductDataModal";


export default function HomePage() {

    const router = useRouter()

    const [products, setProducts] = useState<IProduct[]>([])
    const [opened, { open, close }] = useDisclosure(false);

    const [loading, setLoading] = useState(false)

    useEffect(() => {

        fetch("/api/product/own", {
            method: 'get',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
        }).then(async (res) => {
            const data = await res.json()
            if (res.status == 200) setProducts(data)
        })

    }, [setProducts])

    const onSubmit = async (value: {
        name: string,
        code: string,
        price: number,
        amount: number,
        description: string,
        image: string,
    }) => {

        setLoading(true)

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

        const res = await fetch('/api/product/add', {
            method: 'post',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(value)
        })

        if (res.status === 201) return router.reload()

        setLoading(false)
    }

    return (
        <>
            <Navbar>
                <ProductModalData opened={opened} close={close} onSubmit={onSubmit} loading={loading} />

                <Group grow wrap="nowrap" mb={'md'}>
                    <Button onClick={open} >Agregar</Button>
                </Group>

                <Grid>
                    {products.map((p, index) => {
                        return (
                            <Grid.Col span={{ base: 12, md: 4, lg: 2 }} key={index}>
                                <ProductCard product={p} />
                            </Grid.Col>
                        )
                    })}

                </Grid>

            </Navbar >
        </>
    );
}

export async function getServerSideProps(context: any) {

    try {
        const { req } = context;

        const token = cookie.parse((req && req.headers.cookie) || null)[TOKEN_NAME];

        if (token == null) {
            return {
                redirect: {
                    destination: '/auth/login',
                    permanent: false,
                },
            }
        }

    }
    catch {
        return {
            props: {},
        }
    }

    return {
        props: {},
    }

}