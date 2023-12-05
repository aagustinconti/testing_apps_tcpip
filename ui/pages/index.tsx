import { Navbar } from "@/components/Navbar";
import { ProductCard } from "@/components/ProductCard";
import { TOKEN_NAME } from "@/utils/constants";
import { IProduct } from "@/utils/interfaces";
import { Card, Grid, Text, Image, Group, Badge, NumberFormatter } from "@mantine/core";
import { ChangeEvent, useEffect, useState } from "react";
import cookie from "cookie";


export default function HomePage(props: { logged: boolean }) {

	const [products, setProducts] = useState<IProduct[]>([])

	const getAll = () => {
		fetch("/api/product/all", {
			method: 'get',
			headers: {
				'Accept': 'application/json',
				'Content-Type': 'application/json'
			},
		}).then(async (res) => {
			const data = await res.json()
			setProducts(data)
		})
	}


	useEffect(getAll, [setProducts])

	const onSearch = (event: ChangeEvent<HTMLInputElement>) => {

		console.log(event.target.value.length)

		if (event.target.value.length === 0) {
			return getAll()
		}

		if (event.target.value.length < 3) {
			return
		}

		fetch('/api/product/get', {
			method: 'post',
			headers: {
				'Accept': 'application/json',
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ code: event.target.value, name: event.target.value })
		}).then(async (res) => {
			const data = await res.json()
			setProducts(data)
		})

	}

	return (
		<>
			<Navbar logged={props.logged} onSearchInput={onSearch}>
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