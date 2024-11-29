"use client";

import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { SiInstagram, SiDiscord, SiImessage } from "@icons-pack/react-simple-icons";
import { useUser } from "@/lib/hooks/useUser";
import Markdown from "react-markdown";

interface Pair {
  pairid: number;
  partner: {
    username: string;
    firstName: string;
    lastName: string;
  };
  result?: {
    affection: number;
    vulnerability: number;
    kindness: number;
    other: number;
    negative: number;
    explanation: string;
    rate: number;
    convo: number;
    total: number;
    match_status: number;
  } | null;
}

export default function YourInteractionsTable() {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedPair, setSelectedPair] = useState<Pair | null>(null);
  const [pairs, setPairs] = useState<Pair[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const { user } = useUser();

  useEffect(() => {
    const fetchPairs = async () => {
      if (!user?.username) return;

      try {
        const response = await fetch(`/api/pairs/getUserPairs?username=${user.username}`);
        const data = await response.json();

        if (data.success && data.pairs) {
          setPairs(data.pairs);
        }
      } catch (error) {
        console.error("Failed to fetch pairs:", error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchPairs();
  }, [user?.username]);

  // Calculate match percentage based on result data
  const calculateMatchPercentage = (result: Pair["result"]) => {
    if (!result) return null;
    return Math.round(
      ((result.affection +
        result.vulnerability +
        result.kindness +
        result.other -
        result.negative) /
        result.total) *
        100
    );
  };

  if (isLoading) {
    return (
      <div className="w-full max-w-4xl mx-auto text-center text-white">Loading interactions...</div>
    );
  }

  console.log(pairs);

  return (
    <div className="w-full max-w-4xl mx-auto space-y-10 rounded-xl">
      <h2 className="text-4xl font-extrabold text-center bg-gradient-to-r from-purple-400 via-pink-300 to-red-400 text-transparent bg-clip-text animate-gradient">
        Your Interactions
      </h2>
      <div className="rounded-xl overflow-hidden shadow-lg bg-gradient-to-br from-purple-100 via-pink-100 to-red-100">
        <Table className="border-collapse glow-border">
          <TableHeader>
            <TableRow className="bg-gradient-to-r from-purple-200 via-pink-200 to-red-200">
              <TableHead className="font-bold text-lg text-gray-800 p-4">Name</TableHead>
              <TableHead className="font-bold text-lg text-gray-800 p-4">Match %</TableHead>
              <TableHead className="font-bold text-lg text-gray-800 p-4">Socials</TableHead>
              <TableHead className="font-bold text-lg text-gray-800 p-4">Action</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {pairs.map((pair) => (
              <TableRow key={pair.pairid} className="hover:bg-white/50 transition-colors">
                <TableCell className="font-medium text-lg p-4">
                  {pair.partner.firstName} {pair.partner.lastName}
                </TableCell>
                <TableCell className="p-4">
                  {pair.result ? (
                    <span className="text-2xl font-bold bg-gradient-to-r from-green-500 to-blue-500 text-transparent bg-clip-text">
                      {calculateMatchPercentage(pair.result)}%
                    </span>
                  ) : (
                    <span className="text-gray-500">Pending</span>
                  )}
                </TableCell>
                <TableCell className="p-4">
                  <div className="flex gap-4">
                    <SiInstagram className="w-5 h-5 text-pink-600 cursor-pointer" />
                    <SiDiscord className="w-5 h-5 text-indigo-600 cursor-pointer" />
                    <SiImessage className="w-5 h-5 text-green-600 cursor-pointer" />
                  </div>
                </TableCell>
                <TableCell className="p-4">
                  <Dialog
                    open={isOpen && selectedPair?.pairid === pair.pairid}
                    onOpenChange={setIsOpen}
                  >
                    <DialogTrigger asChild>
                      <Button
                        onClick={() => setSelectedPair(pair)}
                        className="bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white font-bold py-2 px-4 rounded-full transition-all duration-300 transform hover:scale-105"
                      >
                        View Summary
                      </Button>
                    </DialogTrigger>
                    <DialogContent className="sm:max-w-2xl max-h-[80vh] overflow-y-auto bg-gradient-to-br from-purple-100 via-pink-100 to-red-100">
                      <DialogHeader>
                        <DialogTitle className="text-2xl font-bold text-gray-800">
                          Interaction Summary
                        </DialogTitle>
                        <DialogDescription className="text-lg text-gray-600">
                          {pair.partner.firstName} {pair.partner.lastName}
                          {pair.result && ` - ${calculateMatchPercentage(pair.result)}% Match`}
                        </DialogDescription>
                      </DialogHeader>
                      <div className="mt-4 text-gray-700">
                        {pair.result ? (
                          <>
                            <p className="mb-2">Match Analysis:</p>
                            <ul className="list-disc list-inside space-y-1">
                              <li>Affection: {pair.result.affection}/10</li>
                              <li>Vulnerability: {pair.result.vulnerability}/10</li>
                              <li>Kindness: {pair.result.kindness}/10</li>
                              <li>Other Positive Traits: {pair.result.other}/10</li>
                              <li>Negative Aspects: {pair.result.negative}/10</li>
                            </ul>
                            <Markdown className="mt-4 whitespace-pre-wrap">
                              {pair.result.explanation}
                            </Markdown>
                          </>
                        ) : (
                          <p>No interaction data available yet.</p>
                        )}
                      </div>
                    </DialogContent>
                  </Dialog>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}
