
import cookie from "cookie";
import { useRouter } from 'next/router';
import { TOKEN_NAME } from '@/utils/constants';
import { Navbar } from "@/components/Navbar";
import { ProductCard } from "@/components/ProductCard";
import { IProduct } from "@/utils/interfaces";
import { Card, Grid, Text, Image, Group, Badge, NumberFormatter } from "@mantine/core";
import { useEffect, useState } from "react";


export default function HomePage() {

    const [products, setProducts] = useState<IProduct[]>([])

    useEffect(() => {

        fetch("/api/product/all", {
            method: 'get',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
        }).then(async (res) => {
            const data = await res.json()
            console.log(data)
            setProducts(data)
        })

    }, [setProducts])

    return (
        <>
            <Navbar>
                <Grid>
                    {products.map(p => {

                        return (
                            <Grid.Col span={{ base: 12, md: 4, lg: 2 }}>
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