import { useDisclosure } from '@mantine/hooks';
import { AppShell, Burger, Group, UnstyledButton, Title } from '@mantine/core';
import classes from './Navbar.module.css';

import { ReactNode } from 'react';

import {
    IconHome,
    IconSettings,
} from '@tabler/icons-react'
import { useRouter } from 'next/router';

export function Navbar(props: { children: ReactNode }) {
    const [opened, { toggle }] = useDisclosure();
    const router = useRouter()

    return (
        <AppShell
            header={{ height: 60 }}
            navbar={{ width: 300, breakpoint: 'sm', collapsed: { desktop: true, mobile: !opened } }}
            padding="md"
        >
            <AppShell.Header>
                <Group h="100%" px="md">
                    <Burger opened={opened} onClick={toggle} hiddenFrom="sm" size="sm" />
                    <Group justify="space-between" style={{ flex: 1 }}>
                        <Title>
                            Ferreteria SRL
                        </Title>
                        <Group ml="xl" gap={0} visibleFrom="sm">
                            <UnstyledButton className={classes.control} onClick={() => router.push('/')}>Inicio</UnstyledButton>
                            <UnstyledButton className={classes.control} onClick={() => router.push('/admin')}>Administrar</UnstyledButton>
                        </Group>
                    </Group>
                </Group>
            </AppShell.Header>

            <AppShell.Navbar py="md" px={4}>
                <UnstyledButton className={classes.control} onClick={() => router.push('/')}>
                    <IconHome stroke={1.5} className={classes.controlIcon} />
                    <span>Inicio</span>
                </UnstyledButton>
                <UnstyledButton className={classes.control} onClick={() => router.push('/admin')}>
                    <IconSettings stroke={1.5} className={classes.controlIcon} />
                    <span>Administrar</span>
                </UnstyledButton>
            </AppShell.Navbar>

            <AppShell.Main>
                {props.children}
            </AppShell.Main>
        </AppShell>
    );
}
