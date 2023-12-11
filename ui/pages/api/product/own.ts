import { API_URL, TOKEN_NAME } from "@/utils/constants";
import { serialize, parse } from "cookie";
import { NextApiRequest, NextApiResponse } from "next";

export default async function getOwnProducts(req: NextApiRequest, res: NextApiResponse) {
    try {

        const token = parse(req.headers.cookie ?? '')[TOKEN_NAME];

        if (token == undefined) {
            return res.status(401).json({ error: "Not logged in" });
        }

        const url = `${API_URL}/products/get/own`

        const response = await fetch(url, {
            method: 'get',
            headers: {
                'Accept': 'application/json',
                'Authorization': `Bearer ${token}`
            }
        })

        const data = await response.json()
        return res.status(response.status).json(data)

    } catch (err) {
        console.log(err)
        return res.status(500).json("Ocurrio un error, intente de nuevo mas tarde.");
    }
}