import { Suspense } from "react";
import { LoginForm } from "@/components/auth-forms";
import { Card, CardBody, CardHeader } from "@/components/ui/card";
import { getI18n } from "@/i18n/server";

export const metadata = { title: "AP²I" };

export default async function Page() {
  const { d } = await getI18n();
  return (
    <div className="mx-auto max-w-md">
      <Card>
        <CardHeader as="h1" title={<span className="text-xl">{d.auth.loginTitle}</span>} />
        <CardBody>
          <Suspense fallback={<p>{d.common.loading}</p>}><LoginForm /></Suspense>
        </CardBody>
      </Card>
    </div>
  );
}
