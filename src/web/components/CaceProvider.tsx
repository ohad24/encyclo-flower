import { CacheProvider } from '@emotion/react';
import createCache from '@emotion/cache';
import rtl from 'stylis-plugin-rtl';
import { useRouter } from 'next/router';

type Props = {
  children?: JSX.Element;
};

const options = {
  rtl: { key: 'css-ar', stylisPlugins: [rtl] },
  ltr: { key: 'css-en' },
};

export function RtlProvider({ children }: Props) {
  const { locale } = useRouter();
  const dir = locale == 'ar' ? 'rtl' : 'ltr';
  const cache = createCache(options[dir]);
  return <CacheProvider value={cache}>{children};</CacheProvider>;
}
