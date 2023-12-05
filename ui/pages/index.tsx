import { Navbar } from "@/components/Navbar";
import { ProductCard } from "@/components/ProductCard";
import { TOKEN_NAME } from "@/utils/constants";
import { IProduct } from "@/utils/interfaces";
import { Card, Grid, Text, Image, Group, Badge, NumberFormatter } from "@mantine/core";
import { useEffect, useState } from "react";
import cookie from "cookie";


export default function HomePage(props: { logged: boolean }) {

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
			<Navbar logged={props.logged}>
				<Grid>
					{products.map(p => {
						if (p.amount)
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



		return {
			props: { logged: token !== null && token !== undefined },
		}

	}
	catch {
		return {
			props: {},
		}
	}
}