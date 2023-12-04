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