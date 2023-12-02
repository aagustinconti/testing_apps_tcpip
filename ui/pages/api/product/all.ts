import { TOKEN_NAME } from "@/utils/constants";
import { serialize } from "cookie";
import { NextApiRequest, NextApiResponse } from "next";

export default async function getAllProducts(req: NextApiRequest, res: NextApiResponse) {
    try {

        const url = `${process.env.API_URL ?? 'http://127.0.0.1:8000'}/products/get/all`

        const response = await fetch(url, {
            method: 'get',
            headers: {
                'Accept': 'application/json'
            }
        })

        const data = await response.json()
        return res.status(200).json(data)

    } catch (err) {
        console.log(err)
        return res.status(500).json("Ocurrio un error, intente de nuevo mas tarde.");
    }
}