import { TOKEN_NAME } from '@/utils/constants';
import { serialize } from 'cookie'

export default function Logout() {

    return <></>
}

export async function getServerSideProps(ctx: any) {

    ctx.res.setHeader('Set-Cookie', [
        serialize(TOKEN_NAME, '', {
            maxAge: -1,
            path: '/',
        })
    ]);

    return {
        redirect: {
            destination: '/auth/login',
            permanent: false,
        },
    }

}

