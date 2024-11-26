"use client";

import { useState } from "react";
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

interface Interaction {
  id: number;
  name: string;
  matchPercentage: number;
  summary: string;
  socials?: {
    instagram?: string;
    discord?: string;
    phone?: string;
  };
}

const interactions: Interaction[] = [
  {
    id: 1,
    name: "Emma Johnson",
    matchPercentage: 95,
    summary:
      "You and Emma have a lot in common! You both love hiking, enjoy indie music, and are passionate about environmental causes. Your conversations have been filled with laughter and deep discussions about your future goals.",
    socials: {
      instagram: "@emmaj",
      discord: "emmaj#1234",
      phone: "+1234567890"
    }
  },
  {
    id: 2,
    name: "Liam Chen",
    matchPercentage: 88,
    summary:
      "Liam's witty humor perfectly complements your sarcastic jokes. You've bonded over your shared love for sci-fi movies and gourmet cooking. Your chats often run late into the night, exploring topics from quantum physics to philosophy.",
    socials: {
      instagram: "@liamchen",
      discord: "liamchen#5678"
    }
  },
  {
    id: 3,
    name: "Sophia Patel",
    matchPercentage: 92,
    summary:
      "Your connection with Sophia is electric! You both have a passion for dance and have even talked about taking salsa classes together. Your shared interest in travel has led to exciting discussions about future adventures.",
    socials: {
      phone: "+1987654321"
    }
  },
];

export default function YourInteractionsTable() {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedInteraction, setSelectedInteraction] = useState<Interaction | null>(null);

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
            {interactions.map((interaction) => (
              <TableRow key={interaction.id} className="hover:bg-white/50 transition-colors">
                <TableCell className="font-medium text-lg p-4">{interaction.name}</TableCell>
                <TableCell className="p-4">
                  <span className="text-2xl font-bold bg-gradient-to-r from-green-500 to-blue-500 text-transparent bg-clip-text">
                    {interaction.matchPercentage}%
                  </span>
                </TableCell>
                <TableCell className="p-4">
                  <div className="flex gap-4">
                    <SiInstagram className="w-5 h-5 text-pink-600 cursor-pointer" />

                    <SiDiscord 
                      className={`w-5 h-5 ${interaction.socials?.discord ? 'text-indigo-600 cursor-pointer' : 'text-gray-400'}`}
                    />
                    <SiImessage 
                      className={`w-5 h-5 ${interaction.socials?.phone ? 'text-green-600 cursor-pointer' : 'text-gray-400'}`}
                    />
                  </div>
                </TableCell>
                <TableCell className="p-4">
                  <Dialog open={isOpen} onOpenChange={setIsOpen}>
                    <DialogTrigger asChild>
                      <Button
                        onClick={() => setSelectedInteraction(interaction)}
                        className="bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white font-bold py-2 px-4 rounded-full transition-all duration-300 transform hover:scale-105"
                      >
                        View Summary
                      </Button>
                    </DialogTrigger>
                    <DialogContent className="sm:max-w-[425px] bg-gradient-to-br from-purple-100 via-pink-100 to-red-100">
                      <DialogHeader>
                        <DialogTitle className="text-2xl font-bold text-gray-800">
                          Interaction Summary
                        </DialogTitle>
                        <DialogDescription className="text-lg text-gray-600">
                          {selectedInteraction?.name} - {selectedInteraction?.matchPercentage}%
                          Match
                        </DialogDescription>
                      </DialogHeader>
                      <div className="mt-4 text-gray-700">{selectedInteraction?.summary}</div>
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
