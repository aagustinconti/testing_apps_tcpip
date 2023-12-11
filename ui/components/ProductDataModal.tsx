import { IProduct } from "@/utils/interfaces";
import { Button, FileButton, Group, Modal, NumberInput, Stack, TextInput, Textarea, Image } from "@mantine/core";
import { useForm } from "@mantine/form";
import { useRef, useState } from "react";

export default function ProductDataModal(props: {
    title: string,
    buttonText?: string
    opened: boolean,
    close: () => void,
    onSubmit: (
        value: {
            name: string,
            code: string,
            price: number,
            amount: number,
            description: string,
            image: string
        }) => Promise<void> | void,
    loading: boolean
    values?: IProduct
}) {

    const form = useForm({

        initialValues: {
            name: props.values?.name ?? '',
            code: props.values?.product_code ?? '',
            price: props.values?.price ?? 0,
            amount: props.values?.amount ?? 0,
            description: props.values?.description ?? '',
        },

        validate: {
            name: (val: string) => (val.length > 3 ? null : 'El nombre debe tener al menos 3 letras'),
            code: (val: string) => ((val.length < 8 || val.length > 15) ? 'El codigo debe tener entre 8 y 15 digitos' : null),
            price: (val: number) => (val < 0 ? 'El precio debe ser mayor a cero' : null),
            amount: (val: number) => (val < 0 ? 'La cantidad debe ser mayor a cero' : null),
        },

    });

    const [file, setFile] = useState<File | null>(null);
    const [imgPreview, setImgPreview] = useState(props.values?.image ?? '')

    const uploadFile = (file: File | null) => {
        if (file) {

            setFile(file);

            const reader = new FileReader();
            reader.onloadend = () => {
                if (reader.result && typeof reader.result === 'string') {
                    setImgPreview(reader.result)
                };
            };

            reader.readAsDataURL(file);
        }
    }

    const resetRef = useRef<() => void>(null);

    const clearFile = () => {
        setFile(null);
        setImgPreview('')
        form.setFieldValue('image', '')
        resetRef.current?.();
    };

    return (
        <Modal opened={props.opened} onClose={props.close} title={props.title} centered>
            <form onSubmit={form.onSubmit((val) => {
                props.onSubmit({ ...val, image: imgPreview.split(',')[1] })
            })}>
                <Stack>

                    <Group grow wrap="nowrap" >
                        <TextInput
                            required
                            label="Nombre"
                            placeholder="Producto"
                            radius="md"
                            {...form.getInputProps('name')}
                        />

                        <TextInput
                            required
                            label="Codigo"
                            placeholder="XXXXXXXX"
                            radius="md"
                            {...form.getInputProps('code')}
                        />
                    </Group>

                    <Group grow wrap="nowrap" >
                        <NumberInput
                            required
                            label="Precio"
                            radius="md"
                            decimalScale={2}
                            min={0}
                            {...form.getInputProps('price')}
                        />

                        <NumberInput
                            required
                            label="Cantidad"
                            radius="md"
                            min={0}
                            decimalScale={0}
                            {...form.getInputProps('amount')}
                        />
                    </Group>

                    <Textarea
                        label="Descripcion"
                        {...form.getInputProps('description')}
                    />

                    <Group grow wrap="nowrap" >
                        <Stack>
                            <FileButton onChange={uploadFile} accept="image/png,image/jpeg" >
                                {(props) => <Button variant="light" {...props}>{!imgPreview.length ? 'Subir imagen' : 'Remplezar imagen'}</Button>}
                            </FileButton>
                            <Button disabled={(!file && !imgPreview.length)} color="red" onClick={clearFile} variant="light">
                                Quitar imagen
                            </Button>
                        </Stack>

                        <Image
                            src={imgPreview}
                            fit="fill"
                            fallbackSrc='https://www.theironclinic.com/ironc/wp/wp-content/uploads/2018/08/placeholder-600x400.png'
                            h={'100%'}
                        />
                    </Group>


                </Stack>

                <Button fullWidth mt="xl" loading={props.loading} type="submit" variant="light">
                    {props.buttonText ?? 'Crear'}
                </Button>
            </form>
        </Modal>
    )
}