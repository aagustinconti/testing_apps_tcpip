import cookie from "cookie";
import { useRouter } from 'next/router';
import { useState } from 'react';
import { TOKEN_NAME } from '@/utils/constants';
import { useForm } from '@mantine/form';
import {
    TextInput,
    PasswordInput,
    Paper,
    PaperProps,
    Button,
    Stack,
    Center,
    Title,
    Alert
} from '@mantine/core';
import { IconExclamationCircle } from "@tabler/icons-react";

import classes from './login.module.css'

export default function AuthenticationForm(props: PaperProps) {

    const form = useForm({
        initialValues: {
            email: '',
            password: '',
        },

        validate: {
            email: (val: string) => (/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{1,}$/.test(val) ? null : 'Email invalido'),
            password: (val: string) => (val.length < 8 ? 'La contraseña debe tener al menos 8 caracteres' : null),
        },

    });

    const router = useRouter();
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState<string | null>(null)

    const onSubmit = async (value: { email: string, password: string }) => {

        setLoading(true)
        setError(null)

        const response = await fetch("/api/auth/login", {
            method: 'post',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(value)
        })

        const data = await response.json();

        if (response.status != 200) {
            setError(data.errors[0])
            setLoading(false);
            return;
        }

        router.reload();
    }

    return (
        <Center h={'75vh'}>
            <Paper radius="md" p="xl" withBorder {...props}>

                <Title order={2} ta="center" mt="md" mb={25}>
                    Bienvenido a Ferretería SRL
                </Title>

                {error != null && (
                    <Alert variant="light" color="red" mt="md" mb={25} icon={<IconExclamationCircle />} classNames={{ message: classes.message }}>
                        {error}
                    </Alert>
                )}


                <form onSubmit={form.onSubmit(onSubmit)}>
                    <Stack>

                        <TextInput
                            required
                            label="Email"
                            placeholder="usuario@ejemplo.com.ar"
                            radius="md"
                            {...form.getInputProps('email')}
                        />

                        <PasswordInput
                            required
                            label="Contraseña"
                            placeholder="Tu contraseña"
                            radius="md"
                            {...form.getInputProps('password')}
                        />

                    </Stack>

                    <Button fullWidth mt="xl" loading={loading} type="submit">
                        Ingresar
                    </Button>
                </form>
            </Paper>
        </Center>
    );
}

export async function getServerSideProps(context: any) {

    try {
        const { req } = context;

        const token = cookie.parse((req && req.headers.cookie) || '')[TOKEN_NAME];

        if (token != undefined) {
            return {
                redirect: {
                    destination: '/admin',
                    permanent: false,
                },
            }
        }

    }
    catch (e) {
        console.log(e)
    }

    return {
        props: {},
    }

}