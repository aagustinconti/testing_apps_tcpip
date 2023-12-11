import { API_URL, TOKEN_NAME } from "@/utils/constants";
import { parse } from "cookie";
import { NextApiRequest, NextApiResponse } from "next";

export default async function addImage(req: NextApiRequest, res: NextApiResponse) {
    try {

        const token = parse(req.headers.cookie ?? '')[TOKEN_NAME];

        if (token == undefined) {
            return res.status(401).json({ error: "Not logged in" });
        }

        const url = `${API_URL}/image/add`

        const { image_base64 } = req.body

        const response = await fetch(url, {
            method: 'post',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                new_image: {
                    image_base64,
                }
            })
        })

        const data = await response.json()

        if (response.status === 201) {
            return res.status(response.status).json(`/api/image/get/${data}`)
        }

        return res.status(response.status).json(data)

    } catch (err) {
        console.log(err)
        return res.status(500).json("Ocurrio un error, intente de nuevo mas tarde.");
    }
}