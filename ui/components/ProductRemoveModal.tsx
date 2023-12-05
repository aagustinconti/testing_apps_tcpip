import { IProduct } from "@/utils/interfaces";
import { Button, FileButton, Group, Modal, NumberInput, Stack, TextInput, Textarea, Image } from "@mantine/core";
import { useForm } from "@mantine/form";
import { useRouter } from "next/router";
import { useRef, useState } from "react";

export default function ProductRemoveModal(props: {
    opened: boolean,
    close: () => void,
    name: string
    code: string
}) {

    const router = useRouter()

    const remove = async () => {

        const res = await fetch('/api/product/remove/' + props.code, {
            method: 'post',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
        })

        if (res.status === 200) return router.reload()

        console.log(res)

    }

    return (
        <Modal opened={props.opened} onClose={props.close} title={`Borrado de productos`} centered>
            ¿Estas seguro que quieres borrar el producto: {props.name}?

            <Group justify="flex-end" mt="md">
                <Button variant="light" onClick={props.close}>No</Button>
                <Button variant="light" color="red" onClick={remove}>Si</Button>
            </Group>
        </Modal>
    )
}