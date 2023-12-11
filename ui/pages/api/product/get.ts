import { API_URL, TOKEN_NAME } from "@/utils/constants";
import { serialize } from "cookie";
import { NextApiRequest, NextApiResponse } from "next";

export default async function getAllProducts(req: NextApiRequest, res: NextApiResponse) {
    try {

        const { code, name } = req.body

        const url = `${API_URL}/products/get/?code=${code}&name=${name}`

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