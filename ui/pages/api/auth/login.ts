import { API_URL, TOKEN_NAME } from "@/utils/constants";
import { serialize } from "cookie";
import { NextApiRequest, NextApiResponse } from "next";

async function loginHandler(req: NextApiRequest, res: NextApiResponse) {
    try {
        const { email, password } = req.body;

        const url = `${API_URL}/auth/login`

        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: `grant_type=&username=${email}&password=${password}&scope=&client_id=&client_secret=`
        })

        const data = await response.json();

        if (data.access_token) {
            res.setHeader(
                'Set-Cookie',
                serialize(TOKEN_NAME, data.access_token, {
                    httpOnly: true,
                    //secure: process.env.NODE_ENV === "production",
                    sameSite: "lax",
                    maxAge: 1000 * 60 * 60 * 24 * 30,
                    path: "/",
                }));
            return res.status(200).json({
                message: "Login successful",
            });
        } else {
            return res.status(401).json(data);
        }
    } catch (e) {
        console.log(e)
        return res.status(500).json("Ocurrio un error, intente de nuevo mas tarde.");
    }
}

export default loginHandler;