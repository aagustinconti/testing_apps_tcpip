import { API_URL } from "@/utils/constants";
import { NextApiRequest, NextApiResponse } from "next";

export default async function getImage(req: NextApiRequest, res: NextApiResponse) {

    res.setHeader(
        "Cache-Control",
        `public, immutable, no-transform, s-maxage=31536000, max-age=31536000`,
    );
    res.setHeader("content-type", "image/png");


    try {

        const { id } = req.query
        const url = `${API_URL}/image/get?id=${id}`

        const response = await fetch(url, {
            method: 'get',
        })

        const contentType = response.headers.get("content-type") ?? '';
        const arrayBuffer = await response.arrayBuffer();
        const buffer = Buffer.from(arrayBuffer);


        res.setHeader("content-type", contentType);

        return res.status(response.status).send(buffer)

    } catch (err) {
        console.log(err)
        return res.status(500).json("Ocurrio un error, intente de nuevo mas tarde.");
    }
}

export const config = {
    api: {
        externalResolver: true,
    },
}